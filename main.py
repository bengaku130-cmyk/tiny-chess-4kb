S={'P':"KKKKUUUUMMOQLLMPKKKOLJIKLMMGKKKK",
'N':"ACEECGKKEKMNELNOEKMNELLMCGKLACEE",
'B':"GIIIIKKKIKLMILLMIKMMIMMMILKKGIII",
'R':"KKKKLMMM"+"JKKK"*5+"KKKL",
'Q':"GIIJIKKKIKLLJKLLKKLLILLLIKLKGIIJ",
'K':"ECCAECCAECCAECCAGEECIGGGOOKKOQMK"}
V={'P':100,'N':300,'B':320,'R':500,'Q':950,'K':20000}
T={p:tuple(V[p]+5*(ord(s[(i//8)*4+min(i%8,7-i%8)])-75)for i in range(64))for p,s in S.items()}
F=str.maketrans('PNBRQKpnbrqk','pnbrqkPNBRQK')
D={'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,-1,1,10)}
D['Q']=D['K']=D['B']+D['R']
def X(i):return (i//10-2)*8+i%10-1
def G(b,C,E,co=0):
 m=[]
 for i in range(120):
  p=b[i]
  if not p.isupper(): continue
  if p=='P':
   if not co and b[i-10]=='.':
    m.append((i,i-10,'Q' if i<39 else None))
    if i>80 and b[i-20]=='.':m.append((i,i-20,None))
   for d in(-9,-11):
    j=i+d
    if b[j].islower()or j==E:m.append((i,j,'Q' if j<29 else None))
  elif p in D:
   for d in D[p]:
    j=i
    while 1:
     j+=d; c=b[j]
     if c==' 'or c.isupper():break
     if c!='.'or not co:m.append((i,j,None))
     if c.islower()or p in'NK':break
  if p=='K'and not co:
   for t2,r2,e2 in((97,98,(96,97)),(93,91,(92,93,94)),(92,91,(93,92)),(96,98,(95,96,97))):
    if abs(t2-i)==2 and r2 in C and all(b[x]=='.'for x in e2):m.append((i,t2,None))
 return m
def M(P,m):
 b,s,C,E=P; i,j,pr=m; p=b[i]; c=b[j]
 d=T[pr or p][X(j)]-T[p][X(i)]
 if c!='.': d+=T[c.upper()][63-X(j)]
 n=b[:i]+'.'+b[i+1:]
 if p=='P'and j==E and c=='.':
  d+=T['P'][63-X(j+10)]; n=n[:j+10]+'.'+n[j+11:]
 n=n[:j]+(pr or p)+n[j+1:]
 if p=='K' and abs(j-i)==2:
  f=98 if j>94 else 91;t=(i+j)//2
  d+=T['R'][X(t)]-T['R'][X(f)]; n=n[:f]+'.'+n[f+1:]; n=n[:t]+'R'+n[t+1:]
 N=set(C)-{i,j}
 if p=='K':N-={91,98}
 e=i-10 if p=='P' and j==i-20 else 0
 return(n[::-1].translate(F),-(s+d),{119-x for x in N},119-e if e else 0)
ND=0; BG=40000
def Sr(P,dp,a,be):
 global ND; ND+=1; b=P[0]; co=dp<=0
 if co:
  if P[1]>a:a=P[1]
  if a>=be:return a
 bs=a if co else-20000
 for m in sorted(G(b,P[2],P[3],co),key=lambda m:-(V[b[m[1]].upper()]if b[m[1]]!='.'else 0)):
  v=19990 if b[m[1]]=='k'else-Sr(M(P,m),dp-1,-be,-a)
  if v>bs:bs=v
  if v>a:a=v
  if a>=be or ND>BG:break
 return bs
def A(Q):return any(Q[0][x[1]]=='k'for x in G(Q[0],Q[2],Q[3],1))
def FL(P):return(P[0][::-1].translate(F),0,P[2],0)
def RT(P):
 global ND
 ms=[]
 for m in G(P[0],P[2],P[3]):
  if A(M(P,m))or(P[0][m[0]]=='K'and abs(m[1]-m[0])==2 and(A(FL(P))or A(M(P,(m[0],(m[0]+m[1])//2,None))))):continue
  ms.append(m)
 bm=None;dp=1
 while dp<=6:
  ND=0;a=-20000;cb=None
  for m in ms:
   v=19990 if P[0][m[1]]=='k'else-Sr(M(P,m),dp-1,-20000,20000)
   if v>a:a=v;cb=m
  if cb and(ND<=BG or bm is None):bm=cb
  if ND>BG:break
  dp+=1
 return bm
def PF(fen):
 f=fen.split()
 b=' '*20+''.join(' '+''.join('.'*int(c) if c.isdigit() else c for c in r)+' ' for r in f[0].split('/'))+' '*20
 C={q for c,q in(('K',98),('Q',91),('k',28),('q',21))if c in f[2]}
 E=(10-int(f[3][1]))*10+ord(f[3][0])-96 if f[3]!='-' else 0
 rt=f[1]=='b'
 if rt:b=b[::-1].translate(F); C={119-x for x in C}; E=119-E if E else 0
 s=sum(T[c][X(i)]if c.isupper()else-T[c.upper()][63-X(i)] for i,c in enumerate(b) if c.isalpha())
 return(b,s,C,E),rt
ST='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'
P,rt=PF(ST)
for l in open(0):
 t=l.split()
 c=t[0]
 if c=='uci':print('uciok',flush=1)
 elif c=='isready':print('readyok',flush=1)
 elif c=='quit':break
 elif c=='position':
  if t[1]=='startpos':P,rt=PF(ST); mv=t[3:]
  else:
   k=t.index('moves') if 'moves' in t else len(t); P,rt=PF(' '.join(t[2:k])); mv=t[k+1:]
  for u in mv:
   i=(10-int(u[1]))*10+ord(u[0])-96; j=(10-int(u[3]))*10+ord(u[2])-96
   pr=u[4].upper()if len(u)>4 else None
   if rt:i,j=119-i,119-j
   for m in G(P[0],P[2],P[3]):
    if m==(i,j,pr): P=M(P,m); break
   rt=not rt
 elif c=='go':
  if'nodes'in t:BG=int(t[t.index('nodes')+1])
  m=RT(P)
  if m is None:print('bestmove 0000',flush=1)
  else:
   i,j,pr=m
   if rt:i,j=119-i,119-j
   print('bestmove '+chr(96+i%10)+str(10-i//10)+chr(96+j%10)+str(10-j//10)+(pr.lower() if pr else ''),flush=1)