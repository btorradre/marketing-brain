import json,sys,tempfile,unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from store import Store,blank_record
from obsidian_memory import sync,home,remember,context,search,status
from workflow import queue_task,update_task
from performance import save_decision

class MemoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.st=Store(self.root/'_engine/ad-system/data/db.sqlite3',self.root)
        self.r=self.st.save(blank_record('motilli','Memory fixture'),0)
    def tearDown(self):self.tmp.cleanup()
    def note(self):return home(self.st)/'creatives'/f"{self.r['id']}.md"
    def test_auto_sync_new_and_changed_record(self):
        self.assertIn('Memory fixture',self.note().read_text());r=self.st.get(self.r['id']);r['context_notes']='Current selected context';self.st.save(r,r['revision'])
        self.assertIn('Current selected context',self.note().read_text());self.assertEqual(status(self.st)['status'],'synced')
    def test_agent_notes_persist_and_context_retrieves(self):
        x=remember(self.st,self.r['id'],'The current reference uses a different presenter.','fixture observation 2026-09-11')
        p=self.root/x['path'];p.write_text(p.read_text()+'\nManually added in Obsidian.\n')
        r=self.st.get(self.r['id']);r['title']='Updated record';self.st.save(r,r['revision'])
        c=context(self.st,r['id']);self.assertIn('different presenter',c['agent_notes']);self.assertIn('Manually added in Obsidian.',c['agent_notes']);self.assertIn('fixture observation 2026-09-11',c['agent_notes'])
    def test_manual_generated_edit_is_preserved_as_conflict(self):
        self.note().write_text(self.note().read_text()+'\nUnexpected manual edit\n')
        r=self.st.get(self.r['id']);r['title']='New title';self.st.save(r,r['revision'])
        self.assertIn('Unexpected manual edit',self.note().read_text());self.assertEqual(status(self.st)['status'],'conflict');self.assertEqual(context(self.st,r['id'])['revision'],2)
    def test_decisions_and_tasks_refresh_without_creative_revision(self):
        remember(self.st,self.r['id'],'Check presenter versus full-ad scope.','fixture source')
        t=queue_task(self.st,self.r['id'],'research');self.assertIn('Check presenter versus full-ad scope.',Path(t['body']['packet']).read_text())
        update_task(self.st,t['id'],'start','fixture-agent');self.assertIn('Recorded state: working',self.note().read_text())
        d=dict(outcome='insufficient_evidence',measurement_ids=[],**{k:'Fixture '+k for k in ['observation','interpretation','alternative','next_test','fixed','changed']})
        decision=save_decision(self.st,self.r['id'],d);self.assertIn(decision['id'],self.note().read_text());self.assertEqual(self.st.get(self.r['id'])['revision'],1)
    def test_search_brand_scope_and_sources(self):
        remember(self.st,self.r['id'],'Unique calibration mismatch.','Source A')
        other=self.st.save(blank_record('velantra','Unique calibration mismatch'),0)
        hits=search(self.st,'unique calibration','motilli');self.assertTrue(hits);self.assertTrue(all(x['creative_id']==self.r['id'] for x in hits))
        self.assertTrue(any(x['kind']=='notes' for x in hits))
    def test_repeated_sync_no_rewrites(self):
        before=self.note().stat().st_mtime_ns;report=sync(self.st);self.assertEqual(report['written'],0);self.assertEqual(before,self.note().stat().st_mtime_ns)
    def test_rollback_does_not_publish(self):
        previous=status(self.st)['event_id']
        with self.assertRaises(RuntimeError):
            with self.st.connect() as c:self.st.event(c,self.r['id'],'fixture',{});raise RuntimeError('rollback')
        self.assertEqual(status(self.st)['event_id'],previous)
    def test_failed_sync_preserves_committed_record_and_recovers(self):
        r=self.st.get(self.r['id']);r['context_notes']='Must persist'
        with patch('obsidian_memory.sync',side_effect=OSError('simulated write failure')):saved=self.st.save(r,r['revision'])
        self.assertEqual(saved['revision'],2);self.assertEqual(status(self.st)['status'],'error');self.assertEqual(sync(self.st)['status'],'synced');self.assertIn('Must persist',self.note().read_text())
    def test_concurrent_agents_share_latest_snapshot(self):
        def create(i):
            s=Store(self.st.db,self.root);return s.save(blank_record('motilli','Parallel fixture '+str(i)),0)
        with ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(create,range(3)))
        report=sync(self.st);self.assertEqual(report['creatives'],4);self.assertFalse(report['errors'])
        for r in records:self.assertIn(r['title'],(home(self.st)/'creatives'/f"{r['id']}.md").read_text())
    def test_markdown_mirror_reads_without_creating_database(self):
        import shutil
        from obsidian_memory import MarkdownStore
        with tempfile.TemporaryDirectory() as other:
            root=Path(other);db=root/'_engine/ad-system/data/system.sqlite3';db.parent.mkdir(parents=True)
            shutil.copytree(home(self.st),db.parent/'memory')
            mirror=MarkdownStore(db,root);c=context(mirror,self.r['id'])
            self.assertTrue(c['read_only_projection']);self.assertFalse(db.exists())
            remember(mirror,self.r['id'],'Mirror observation','Mirror fixture')
            self.assertIn('Mirror observation',context(mirror,self.r['id'])['agent_notes'])
            self.assertTrue(search(mirror,'Mirror observation','motilli'));self.assertFalse(db.exists())
            with self.assertRaises(ValueError):sync(mirror)
if __name__=='__main__':unittest.main()
