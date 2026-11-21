import sys
V={'P':100,'N':310,'B':330,'R':500,'Q':950,'K':20000,'.':0}
W="FFFFsvxxUX[bJLQXFHNTGHIKFFD<FFFF(7<<7AFH>HNPAHPRAHNP>HKL7AFF-:<>>DDDDFFFDHJKDJJLDJKLEKJJDLGG>DAAHHKKPRRRFFHHDFFFAFFFAFFF>DFHDFHKADDFDFFFDFHHDFHHDFHHDHHHAFHF>ADF((((--*(20-*420-7420><74KHA<PUKA"
P={}
for n,x in enumerate('PNBRQK'):
 P[x]=[0]*120
 for i in range(64):r,f=divmod(i,8);P[x][21+r*10+f]=V[x]+2*ord(W[n*32+r*4+min(f,7-f)])-140
A=(-10,-1,1,10,-11,-9,9,11)
D={'P':(-10,-20,-11,-9),'N':(-21,-19,-12,-8,8,12,19,21),'B':A[4:],'R':A[:4],'Q':A,'K':A}
M=30000
def G(p,q=0):
 B,s,c,e,k=p
 for i,x in enumerate(B):
  if x.isupper():
   for d in D[x]:
    j=i+d
    while 1:
     y=B[j]
     if y.isspace():break
     if y.isupper():
      if x=='R'and y=='K'and(i,d)in((91,1),(98,-1))and c[i>91]and not q:yield j,j-2*d
      break
     if x=='P':
      if d in(-10,-20)and y!='.':break
      if d==-20 and(i<81 or B[i-10]!='.'):break
      if d in(-11,-9)and y=='.'and j!=e and j not in k:break
     if y!='.'or not q or j in k or x=='P'and(j==e or j<30):yield i,j
     if x in'PNK'or y!='.':break
     j+=d
def E(p,m,r='Q'):
 B,s,c,e,k=p;i,j=m;x=B[i];y=B[j]
 v=P[x][j]-P[x][i]
 if y!='.':v+=P[y.upper()][119-j]
 if x=='K'and abs(j-i)==2:v+=P['R'][(i+j)//2]-P['R'][91 if j<i else 98]
 if x=='P':
  if j<30:v+=P[r][j]-P['P'][j]
  if j==e:v+=P['P'][109-j]
 return v
def Z(p,m,r='Q'):
 B,s,c,e,k=p;i,j=m;x=B[i];v=E(p,m,r)
 b=list(B);b[j]=x;b[i]='.';n=0;o=()
 c=[c[t]and(91,98,21,28)[t]not in m for t in range(4)]
 if x=='K':
  c[0]=c[1]=0
  if abs(j-i)==2:o=(i,(i+j)//2);b[o[1]]='R';b[91 if j<i else 98]='.'
 if x=='P':
  if j<30:b[j]=r
  if j-i==-20:n=i-10
  if j==e:b[j+10]='.'
 return(''.join(b)[::-1].swapcase(),-s-v,tuple(c[::-1]),119-n,tuple(119-t for t in o))
def O(p):B,s,c,e,k=p;return B[::-1].swapcase(),-s,c[::-1],0,()
def X(p):
 B,s,c,e,k=p
 return any(B[j]=='k'or j in k and(B[i]!='P'or(j-i)%10)for i,j in G(p,1))
def S(p,d,a,b):
 global N
 N+=1
 if N>L:raise KeyError
 B,s,c,e,k=p;f=-M;d=max(d,0);o=a
 if d<1:
  if s>=b:return s
  a=max(a,s);f=s
 u,v=Y.get((p,d),(-M,M))
 if u>=b:return u
 if v<=a:return v
 if d>2:
  t=-S(O(p),d-3,-b,1-b)
  if t>=b:return t
 h=T.get(p)
 for n,m in enumerate(sorted(G(p,d<1),key=lambda m:(m!=h,-(V[B[m[1]].upper()]*20-V[B[m[0]]]if B[m[1]]!='.'else E(p,m)-M)))):
  i,j=m
  if B[j]=='k'or j in k and(B[i]!='P'or(j-i)%10):return M
  q=Z(p,m);r=d>2 and n>3 and B[j]=='.'
  t=-S(q,d-1-r,-b,-max(a,f))
  if r and t>max(a,f):t=-S(q,d-1,-b,-max(a,f))
  if t>f:
   f=t;T[p]=m
   if f>=b:break
 if f==-M and d>0:f=(1-M)*X(O(p))
 f=f-(f>M/2)+(f<-M/2);Y[p,d]=(f if f>o else-M,f if f<b else M)
 return f
def R(p,n,z):
 global N,L,T,Y
 T={};Y={};N=0;L=1e9
 ms=[m for m in G(p)if not X(Z(p,m))];bm=ms[0]if ms else None
 for d in range(1,z+1):
  try:
   a=-M-1
   for m in ms:
    t=-S(Z(p,m),d-1,-M,-a)
    if t>a:a=t;g=m
   bm=g;ms.remove(g);ms.insert(0,g)
  except KeyError:break
  L=n
  if N>=n:break
 return bm
Q=lambda t:ord(t[0])+4-10*int(t[1])
U=lambda i:chr(i%10+96)+str(10-i//10)
p=None
for l in sys.stdin:
 w=l.split()
 if not w:continue
 if w[0]=='uci':print('uciok')
 elif w[0]=='isready':print('readyok')
 elif w[0]=='quit':break
 elif w[0]=='position':
  F=w[2:8]if w[1]=='fen'else['rnbqkbnr/'+'p'*8+'/8'*4+'/'+'P'*8+'/RNBQKBNR','w','KQkq','-']
  B=' '*20
  for r in F[0].split('/'):
   for x in '12345678':r=r.replace(x,'.'*int(x))
   B+=' '+r+'\n'
  B+=' '*20
  s=sum(P[x][i]if x.isupper()else-P[x.upper()][119-i]for i,x in enumerate(B)if x.isalpha())
  p=(B,s,tuple(x in F[2]for x in'QKqk'),0,());b=F[1]=='b'
  e=Q(F[3])if F[3]!='-'else 0
  p=O(p)[:3]+(119-e,())if b else p[:3]+(e,())
  if'moves'in w:
   for u in w[w.index('moves')+1:]:
    i,j=Q(u[:2]),Q(u[2:4])
    if b:i,j=119-i,119-j
    p=Z(p,(i,j),u[4:].upper()or'Q');b=not b
 elif w[0]=='go':
  n=int(w[w.index('nodes')+1])if'nodes'in w else 40000
  z=int(w[w.index('depth')+1])if'depth'in w else 99
  m=R(p,n,z)
  i,j=m or(0,0);print('bestmove',U(119-i if b else i)+U(119-j if b else j)+('q'if p[0][i]=='P'and j<30 else'')if m else'0000')
 sys.stdout.flush()
