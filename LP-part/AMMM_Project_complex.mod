/*********************************************
 * OPL 12.8.0.0 Model
 * Author: joanpratsicart
 * Creation Date: May 2, 2019 at 6:46:45 PM
 *********************************************/


//input data
int providers = ...;
int wr =...;
range P = 1..providers;
int available_workers[p in P] = ...;
int cost_contract[p in P] = ...;
int country[p in P] = ...;
int cost_workers[p in P] = ...;
int cost_1[p in P] = ...;
int cost_2[p in P] = ...;
int cost_3[p in P] = ...;



//Decision variables
dvar int w[p in P]; //noraml workers of a provider
dvar int ex[p in P]; //extra workers of a provider
dvar boolean h[p in P]; //half of the workers of a provider are used
dvar boolean a[p in P]; //all of the workers of a provider are used
dvar boolean b5[p in P]; // at least 5 workers of a provider are used
dvar boolean b10[p in P]; // at least 10 workers of a provider are used



//Objective function
minimize
  sum (p in P) (w[p]*cost_workers[p]+((1-b5[p])*w[p]+b5[p]*5)*cost_1[p]+((1-b10[p])*(w[p]-5)
						+(b10[p])*(10))*cost_2[p]+(b10[p]*(w[p]-10))*cost_3[p]);


//Constraints
subject to{
  forall (p in P)
   	w[p] == (a[p]*available_workers[p]+ex[p])+(h[p]*0.5*available_workers[p]); //each providers provides 0% or 50% or 100% of the available workers + extra
  forall (p in P)
   	ex[p] <= available_workers[p]*a[p]; //ensrure that we only can get extra workers when we alredy get al the workers of a determinated provider
  forall (p in P)
   	h[p]+a[p] <= 1; //we just can get all or the half or the 0 but not all of them
  forall (p in P)
   	w[p]>=5*b5[p]; //b5 can't be 1 if there are less than 5 workers
  forall (p in P)
   	w[p]>=10*b10[p]; //b10 can't be 1 if there are less than 5 workers
  forall (p in P)
   	w[p]-5<=(wr-5)*b5[p]; //b5 have to be one if there are more than five workers 
  forall (p in P)
   	w[p]-10<=(wr-10)*b10[p]; //b10 have to be one if there are more than five workers
  forall (p in P)
   	b5[p]>=b10[p];  // if b10 is one then b5 have to be also one
  forall(p1 in P, p2 in P:p1 < p2 && country[p1]==country[p2])
	h[p1]+a[p1]+h[p2]+a[p2]<=1;  //there can't be two providers form the same country
  sum (p in P) w[p] == wr; // the sum of all the workers proviede by the providers must be equal to the workers requested
  forall (p in P){
    w[p] >= 0;
   	ex[p] >= 0;//ensure that all variables are positive
   	h[p] >= 0;
   	a[p] >= 0;
   	b5[p] >= 0;
   	b10[p] >= 0;
  }   
}

//Post processing data
execute {
 	writeln("In order to hire "+wr+" at the minimum cost the best providers are:");\
 	writeln(w)
  	for (var p in P)	
  		if (w[p] >=1) writeln("provider "+ p +" from the country " + country[p] + " with " + w[p] + " workers, from which  "+ex[p]+"  are extra workers");	 
 } 