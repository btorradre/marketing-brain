def lua(x):
 if isinstance(x,str): return '[=['+x+']=]'
 if isinstance(x,bool): return str(x).lower()
 if isinstance(x,(int,float)): return str(x)
 if isinstance(x,list): return '{'+','.join(lua(v) for v in x)+'}'
 if isinstance(x,dict): return '{'+','.join('[ '+lua(k)+' ]='+lua(v) for k,v in x.items())+'}'
 raise TypeError(type(x))
