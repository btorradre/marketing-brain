import copy, json, sys, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from store import Store, Invalid, Conflict, blank_record, digest, packed
from workflow import qa, transition, compare, queue_task, update_task, task_view
from performance import import_csv, measurements, aggregate, analyze, save_decision, next_iteration, operations
from server import make_server
from inventory import sync_brand

SETTINGS=dict(brand='motilli',platform='meta',account_id='test-account',currency='USD',attribution='7d-click',conversion_event='purchase',click_definition='link-clicks',hook_definition='3s_views/impressions',hold_definition='thruplays/3s_views')
HEADER='ad_id,date_start,date_end,spend,purchases,impressions,clicks,revenue,views_3s,thruplays\n'
CSV=HEADER+'ad1,2026-09-01,2026-09-01,100,2,1000,10,200,300,100\n'+'ad1,2026-09-02,2026-09-02,20,2,100,20,100,50,20\n'
class SystemTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.st=Store(self.root/'_engine/ad-system/data/test.sqlite3',self.root)
        self.folder=self.root/'brands/motilli/creative/TEST';self.folder.mkdir(parents=True)
        self.plan=self.folder/'editing-plan.md';self.plan.write_text('Test plan fixture; not production.')
        self.media=self.folder/'final.mp4';self.media.write_bytes(b'test-media-bytes-not-a-real-ad')
        r=blank_record();r.update(title='Test concept',product='Test product',context_notes='Synthetic test only',script='Test narration',editing_plan=str(self.plan),cutroom_url='http://localhost/test')
        r['strategy']={k:'Test '+k for k in r['strategy']};r['strategy']['format']='ugc'
        r['hooks']=[dict(id='H1',line='Test hook',visual='Test action',test='Test variable')]
        keys=['line','action','story_function','medium','placement','why_line','viewer_response','style_fit','why_here','cut_cue','transition_in','transition_out','source_route']
        r['beats']=[dict(id='B1',duration=3,asset_id='A1',**{k:'test' for k in keys})]
        r['assets']=[dict(id='A1',path=str(self.media),origin='brand-provided',inspection='Test inspection')]
        self.r=self.st.save(r,0)
    def tearDown(self):self.temp.cleanup()
    def exp(self):return self.st.register_export(self.r['id'],str(self.media),self.r['revision'],'H1')
    def bind(self):
        e=self.exp();self.st.bind('meta','test-account','ad1',e['id']);return e
    def test_revision_conflict_and_persistence(self):
        new=copy.deepcopy(self.r);new['title']='Changed';saved=self.st.save(new,1)
        self.assertEqual(saved['revision'],2);self.assertEqual(self.st.get(new['id'],1)['title'],'Test concept')
        with self.assertRaises(Conflict):self.st.save(self.r,1)
        self.assertEqual(Store(self.st.db,self.root).get(new['id'])['title'],'Changed')
    def test_quote_fidelity(self):
        r=copy.deepcopy(self.r);r['evidence']=[dict(id='Q1',kind='quote',text='Exact words.',source_excerpt='Exact words.',source_url='https://example.test/source')]
        r=self.st.save(r,1);r['evidence'][0]['text']='Changed words.'
        with self.assertRaises(Invalid):self.st.save(r,2)
    def test_lock(self):
        r=copy.deepcopy(self.r);r['narration_lock']=dict(hash=digest(r['script']));r=self.st.save(r,1);r['script']='Different'
        with self.assertRaises(Invalid):self.st.save(r,2)
        self.assertIsNone(self.st.save(r,2,unlock_reason='Synthetic user-authorized revision')['narration_lock'])
    def test_scene_reasons_and_tiktok(self):
        r=copy.deepcopy(self.r);r['beats'][0]['why_here']=''
        self.assertIn('beats.B1.why_here',[x['field'] for x in qa(self.st,r,'production')['checks'] if x['verdict']=='FAIL'])
        r=copy.deepcopy(self.r);r['assets'][0].update(specialization='tiktok-extreme',entry_ev=5,peak_ev=5,rawness=4,text_status='text-visible')
        self.assertEqual(qa(self.st,r,'assets')['verdict'],'FAIL')
        r['assets'][0].update(text_status='verified-clean',action_match='verified',frame_audit='all selected frames inspected')
        self.assertNotEqual(qa(self.st,r,'assets')['verdict'],'FAIL')
    def test_media_review_staleness_and_stage(self):
        self.st.add_review(self.r['id'],'human',dict(reviewer='Tester',artifact_path=str(self.media),verdict='PASS',notes='Test only'),1)
        self.assertNotEqual(qa(self.st,self.r,'delivery')['verdict'],'FAIL')
        r=transition(self.st,self.r['id'],'ready',1)
        self.assertNotEqual(qa(self.st,r,'delivery')['verdict'],'FAIL')
        r['script']='Changed';r=self.st.save(r,r['revision'])
        self.assertIn('finished_review',[x['field'] for x in qa(self.st,r)['checks'] if x['verdict']=='FAIL'])
    def test_changed_media_invalidates_review(self):
        self.st.add_review(self.r['id'],'human',dict(reviewer='Tester',artifact_path=str(self.media),verdict='PASS',notes='Test only'),1)
        self.media.write_bytes(b'changed')
        self.assertEqual(qa(self.st,self.r)['verdict'],'FAIL')
    def test_exact_export_binding(self):
        e=self.bind();self.assertEqual(self.exp()['id'],e['id'])
        self.media.write_bytes(b'changed');e2=self.exp()
        with self.assertRaises(Invalid):self.st.bind('meta','test-account','ad1',e2['id'])
        with self.assertRaises(Invalid):self.st.bind('meta','test-account','ad2',e['id'])
        self.assertEqual(self.st.resolve_binding('meta','test-account','ad1')['revision'],1)
    def test_ratios_from_totals_and_idempotence(self):
        self.bind();a=import_csv(self.st,CSV,SETTINGS);b=import_csv(self.st,CSV,SETTINGS)
        self.assertEqual(a['id'],b['id']);self.assertEqual(len(measurements(self.st)),2)
        g=analyze(self.st)['groups'][0]
        self.assertEqual(g['metrics']['cpa'],30);self.assertAlmostEqual(g['metrics']['ctr'],30/1100*100);self.assertEqual(g['totals']['spend'],120)
    def test_duplicate_overlap_atomic(self):
        self.assertEqual(import_csv(self.st,CSV+CSV.splitlines()[1]+'\n',SETTINGS)['body']['status'],'rejected');self.assertEqual(measurements(self.st),[])
        import_csv(self.st,CSV,SETTINGS)
        self.assertEqual(import_csv(self.st,HEADER+'ad1,2026-09-01,2026-09-03,100,2,1000,10,200,300,100\n',SETTINGS)['body']['status'],'rejected')
        self.assertEqual(len(measurements(self.st)),2)
    def test_missing_and_zero_denominators(self):
        c='ad_id,date_start,date_end,spend,purchases,impressions,clicks\na,2026-09-01,2026-09-01,0,0,0,0\n'
        import_csv(self.st,c,SETTINGS);g=aggregate(measurements(self.st))
        self.assertTrue(all(v is None for v in g['metrics'].values()));self.assertIsNone(g['totals']['revenue'])
    def test_mixed_settings_headers_and_values(self):
        bad=CSV.replace('ad_id,','ad_id,ad_id,',1);self.assertEqual(import_csv(self.st,bad,SETTINGS)['body']['status'],'rejected')
        bad=CSV.replace('100,2','nan,2',1);self.assertEqual(import_csv(self.st,bad,SETTINGS)['body']['status'],'rejected')
        import_csv(self.st,CSV,SETTINGS);s={**SETTINGS,'currency':'EUR'};import_csv(self.st,CSV,s)
        with self.assertRaises(Invalid):aggregate(measurements(self.st))
        bad='ad_id,date_start,date_end,spend,purchases,impressions,clicks,currency\na,2026-09-01,2026-09-01,1,1,1,1,EUR\n'
        self.assertEqual(import_csv(self.st,bad,SETTINGS)['body']['status'],'rejected')
    def test_unmatched_rejoin_and_brand_safety(self):
        import_csv(self.st,CSV,SETTINGS);self.assertEqual(len(analyze(self.st)['unmatched']),2)
        self.bind();self.assertEqual(analyze(self.st)['unmatched'],[])
        other=blank_record('velantra','Other');other=self.st.save(other,0);ex=self.st.register_export(other['id'],str(self.media),1,'')
        with self.assertRaises(Invalid):self.st.bind('meta','test-account','ad1',ex['id'])
        settings={**SETTINGS,'account_id':'other'};import_csv(self.st,CSV,settings)
        with self.assertRaises(Invalid):self.st.bind('meta','other','ad1',ex['id'])
    def test_decision_lineage(self):
        body={k:'Test '+k for k in ['observation','interpretation','alternative','next_test','fixed','changed']};body['outcome']='iterate'
        with self.assertRaises(Invalid):save_decision(self.st,self.r['id'],body)
        self.bind();import_csv(self.st,CSV,SETTINGS);body['measurement_ids']=[x['id'] for x in measurements(self.st)]
        d=save_decision(self.st,self.r['id'],body);child=next_iteration(self.st,d['id'],'Next test')
        self.assertEqual(child['parent_revision'],1);self.assertEqual(child['decision_id'],d['id']);self.assertEqual(child['script'],'');self.assertEqual(child['strategy']['changed'],body['changed'])
    def test_tasks_dependency_and_reconciliation(self):
        t=queue_task(self.st,self.r['id'],'research');self.assertEqual(queue_task(self.st,self.r['id'],'research')['id'],t['id'])
        child=queue_task(self.st,self.r['id'],'concept',[t['id']])
        with self.assertRaises(Invalid):update_task(self.st,child['id'],'start','test')
        update_task(self.st,t['id'],'start','test');update_task(self.st,t['id'],'submitted',handle=dict(provider='test',id='actual-fixture',verified_at='2026-09-11'))
        with self.assertRaises(Invalid):update_task(self.st,t['id'],'cancelled')
        update_task(self.st,t['id'],'reconcile',receipt=dict(state='missing',observation='Test job not found'))
        update_task(self.st,t['id'],'start','test');update_task(self.st,t['id'],'done',receipt=dict(path=str(self.plan),observation='Completed test fixture'))
        self.assertEqual(update_task(self.st,child['id'],'start','test')['body']['state'],'working')
    def test_stale_tasks(self):
        t=queue_task(self.st,self.r['id'],'research');r=copy.deepcopy(self.r);r['title']='New';self.st.save(r,1)
        with self.assertRaises(Conflict):update_task(self.st,t['id'],'start','test')
    def test_path_containment_and_symlinks(self):
        outside=self.root/'secret.txt';outside.write_text('test')
        with self.assertRaises(Invalid):self.st.safe_file(outside)
        symlink=self.folder/'link.txt';symlink.symlink_to(outside)
        with self.assertRaises(Invalid):self.st.safe_file(symlink)
        hidden=self.folder/'.private.txt';hidden.write_text('test')
        with self.assertRaises(Invalid):self.st.safe_file(hidden)
    def test_inventory_conservative_idempotent(self):
        a=sync_brand(self.st);b=sync_brand(self.st)
        self.assertIn('TEST',a['changed_creatives']);self.assertEqual(b['changed_creatives'],[])
        r=self.st.get('TEST');self.assertFalse(r['script']);self.assertFalse(r['editing_plan']);self.assertEqual(r['stage'],'intake')
    def test_comparison_and_operations(self):
        r=copy.deepcopy(self.r);r['id']='Other';r['strategy']['format']='podcast'
        self.assertEqual(compare([self.r,r])[0]['classification'],'same argument: execution/copy iteration')
        self.assertIsNone(operations(self.st)['valid_test_coverage']);self.bind();import_csv(self.st,CSV,SETTINGS)
        self.assertEqual(operations(self.st)['valid_test_coverage'],1)
    def test_stage_checks_cannot_be_bypassed(self):
        r=copy.deepcopy(self.r);r['stage']='ready'
        with self.assertRaises(Invalid):self.st.save(r,1)
        with self.assertRaises(Invalid):transition(self.st,self.r['id'],'live',1)
        self.bind();self.st.add_review(self.r['id'],'human',dict(reviewer='Tester',artifact_path=str(self.media),verdict='PASS',notes='Test only'),1)
        r=transition(self.st,self.r['id'],'live',1)
        r['script']='Changed content';r=self.st.save(r,r['revision']);self.assertEqual(r['stage'],'review')
        self.st.add_review(r['id'],'human',dict(reviewer='Tester',artifact_path=str(self.media),verdict='PASS',notes='Test only'),r['revision'])
        with self.assertRaises(Invalid):transition(self.st,r['id'],'live',r['revision'])
    def test_invalid_calibration_and_scores(self):
        r=copy.deepcopy(self.r);r['calibration']['accepted']=1
        with self.assertRaises(Invalid):self.st.save(r,1)
        r=copy.deepcopy(self.r);r['assets'][0]['entry_ev']=6
        with self.assertRaises(Invalid):self.st.save(r,1)
        r=copy.deepcopy(self.r);r['assets'][0]['entry_ev']='5'
        with self.assertRaises(Invalid):self.st.save(r,1)
    def test_http_token_revision_and_range(self):
        server=make_server(self.st,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}'
        try:
            data=json.load(urllib.request.urlopen(base+'/api/bootstrap'));token=data['token']
            body=json.dumps(dict(action='create',title='HTTP test',brand='motilli')).encode()
            with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(urllib.request.Request(base+'/api/action',data=body))
            self.assertEqual(e.exception.code,403)
            req=urllib.request.Request(base+'/api/action',data=body,headers={'X-Creative-Token':token,'Content-Type':'application/json'});created=json.load(urllib.request.urlopen(req));self.assertEqual(created['revision'],1)
            req=urllib.request.Request(base+'/api/file?path='+urllib.parse.quote(str(self.media)),headers={'Range':'bytes=0-3'})
            response=urllib.request.urlopen(req);self.assertEqual(response.status,206);self.assertEqual(response.read(),b'test')
            self.assertEqual(urllib.request.urlopen(base+'/').status,200)
        finally:server.shutdown();server.server_close();thread.join()
if __name__=='__main__':unittest.main(verbosity=2)
