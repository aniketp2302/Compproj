import random
import math

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False
def ftext(s,l,q):#Creates the f function fr the l length subtext whixh has starting index as 0.
	i=0
	f=0
	while i<l:#We have a loop  which happens l times
		f=(f+(((ord(s[i])-65)%q)*pow(26,l-i-1,q))%q)%q#Here for each arithmetic operation we are always taking mod q and always keeping our number less than q thus each operation is taking logq time and thus as the operations are happening l times, the time complexity comes out to be l.log(q)
		i=i+1
	return f
	#Thus we get time complexity as O(l.logq) an space complexity as O(log q).
def fpattern(s,q):
	l=len(s)
	i=0
	ind=-1
	mul=-1
	f=0
	while i<l:
		if s[i]=='?':#Here whenever a '?' is coming it is storing the index of it in the pattern and for f it is taking it's value as 0.
			ind=i#This will take logm space which is lesser than logn so it works.
			mul=pow(26,l-i-1,q)#This takes O(log q) space as it is a number less than q.
			i=i+1
		else:
			f=(f + (((ord(s[i])-65)%q)*pow(26,l-i-1,q))%q)%q
			i=i+1
	return [f,ind,mul]
	#With a similar time complexity and space complexity analysis to that of ftext we get time complexity as O(m.logq) and space complexity as O(logn +logq).
#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatch(q,p,x)

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	q = randPrime(N)
	return modPatternMatchWildcard(q,p,x)

# return appropriate N that satisfies the error bounds
def findN(eps,m):
	#We know that a false positive occurs when lets say ftext=a and fpattern=b, and when a!=b but |a-b|modq==0.
	#The probability of this is total number of such q/total number of primes. We know that |a-b| can be maximum 26**m, Thus maximum number of q is m*log26
	#We know that this probability should be less Than epsilon and we know that number of primes =N/2logN thus we get (N/logN)>(2*m*log26/eps)
	#We know that N**(1/2)>logN. Thus N/logN>N**(1/2)
	#So if we take N**(1/2)==ceil((2*m*log26/eps)), the inequality holds. Thus we take this as our N
	return (((2*m*(math.log(26,2)))**2)//(eps**2))+1
# Return sorted list of starting indices where p matches x
def modPatternMatch(q,p,x):
	n=len(p)
	f=ftext(x,n,q)#This takes mlogq time and log q space.
	fp=fpattern(p,q)[0]
	i=0
	if f==fp:#Checking at i==0
		l=[0]
	else:
		l=[]
	while i<(len(x)-n):#Here i starts from 0 and goes till n-m-1. So loop runs n-m times.
		f=(f-(((ord(x[i])-65)%q)*pow(26,n-1,q))%q)%q #Here we had calculated f for the subtext of length m starting from the index i. We are first subtracting the contribution of ith index of text.
		f=(f*(26%q))%q#We are multiplying the remaining f with 26(and taking mod)
		f=(f+(ord(x[i+n])-65)%q)%q#We are in the end adding the contribution of (i+m)th index. This thus makes the f for the subtext of length m whose index starts at i+1.All these arithmetic operations have been done on number so that will take logq time. Thus the total time complexity comes to O((n-m)logq)
		#As we are only modifying one f and not making f again and again we get space complexity as O(logn+logq+K) instead of O(logn+nlogq +k).
		if f==fp:#If the functions are equal we are appending index to the list.
			l.append(i+1)
		i=i+1
	return l
	#The total time complexity comes to O((n-m)logq)+O(mlogq) which comes to O(nlogq)
	#Thus space complexity is O(logq+logn+k)
# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q,p,x):#The space and time complexity is almost exactly similar to that of modpatternmatch
	n=len(p)
	f=ftext(x,n,q)
	fp=fpattern(p,q)[0]
	mul=fpattern(p,q)[2]
	ind=fpattern(p,q)[1]
	i=0
	if ind == -1:
		return modPatternMatch(q,p,x)
	if f==fp:
		l=[0]
	else:
		l=[]
	while i<(len(x)-n):
		f=(f-(((ord(x[i])-65)%q)*pow(26,n-1,q))%q)%q
		f=(f*(26%q))%q
		f=(f+(ord(x[i+n])-65)%q)%q
		if (f-(((ord(x[i+ind+1])-65)%q)*(mul))%q)%q==fp:#This is almost the only difference between modpattern and wildcard. Here instead of directly comparing f of text with f of pattern we are subtracting whatever the contribution of ith index was in ftext because we had taken contribution of '?' as 0.Note that the subtraction is just one arithmetic operation of logq time and O(1) space so it wont vchange the time and spavce complexity.
			l.append(i+1)
		i=i+1
	return l