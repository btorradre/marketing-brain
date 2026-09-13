#!/usr/bin/env python3
"""Retrieve Nuora's completed TrendTrack transcripts; preserve raw API responses."""
import json, pathlib, urllib.request, urllib.error, time, datetime, ssl
import certifi
ROOT=pathlib.Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
BRAND='8bff2239-0790-4f87-a97e-15434c0fc9b6'

def get_key():
 for line in (WORKSPACE/'.env').read_text().splitlines():
  if line.strip().startswith('TRENDTRACK_API_KEY='):return line.split('=',1)[1].strip().strip('"\'')
 raise RuntimeError('TRENDTRACK_API_KEY missing')

def rpc(method,params,label):
 req=urllib.request.Request('https://api.trendtrack.io/v1/mcp',data=json.dumps({'jsonrpc':'2.0','id':label,'method':method,'params':params}).encode(),headers={'Authorization':'Bearer '+get_key(),'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
 try:
  with urllib.request.urlopen(req,timeout=90,context=ssl.create_default_context(cafile=certifi.where())) as response:
   body=response.read().decode();headers={k:v for k,v in response.headers.items() if k.lower().startswith(('x-usage','x-credit','x-rate'))}
 except urllib.error.HTTPError as e:
  raise RuntimeError('TrendTrack HTTP '+str(e.code)) from None
 if body.lstrip().startswith('{'):data=json.loads(body)
 else:
  messages=[json.loads(x[5:].strip()) for x in body.splitlines() if x.startswith('data:')];data=next(x for x in messages if x.get('id')==label)
 (ROOT/'raw'/f'{label}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 if data.get('error') or data.get('result',{}).get('isError'):raise RuntimeError(str(data.get('error') or data['result'])[:600])
 return data,headers

def call(name,args,label):return rpc('tools/call',{'name':name,'arguments':args},label)

if __name__=='__main__':
 rpc('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'brooks-copy-research','version':'1.0'}},'initialize')
 data,_=rpc('tools/list',{},'tools')
 print('tools',len(data['result']['tools']))
 data,_=call('usage_get',{},'usage-start');print(json.dumps(data['result'].get('structuredContent',{}))[:1600])
 data,headers=call('get_brandtracker_transcripts',{'brandtracker_id':BRAND,'time_period':'last1y','page':1,'limit':50,'sort_by':'usageCount','order':'desc'},'transcripts-year-page-1')
 s=data['result']['structuredContent'];print('PAGE1',len(s.get('data',[])),'META',{k:v for k,v in s.items() if k!='data'},'COST',headers)
