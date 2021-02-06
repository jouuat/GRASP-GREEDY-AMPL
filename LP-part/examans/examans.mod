/*********************************************
 * OPL 12.6.0.0 Model
 * Author: oliveras
 * Creation Date: Apr 4, 2019 at 3:20:29 PM
 *********************************************/

 //input data
int providers = ...;
int wr =...;
range P = 1..providers;
int available_workers[p in P] = ...;
int cost_contract[p in P] = ...;
int country[p in P] = ...;
int cost_workers[p in P] = ...;
int cost_1 = ...;
int cost_2 = ...;
int cost_3 = ...;



//Decision variables
dvar int w[p in P]; //normal workers of a provider
dvar int ex[p in P]; //extra workers of a provider
dvar boolean h[p in P]; //half of the workers of a provider are used
dvar boolean a[p in P]; //all of the workers of a provider are used
dvar int w5[p in P]; // at least 5 workers of a provider are used
dvar int w10[p in P]; // at least 10 workers of a provider are used



//Objective function
minimize
  sum (p in P) ((a[p]+h[p])*cost_contract[p]+cost_workers[p]*w[p]+(w[p]*cost_1+w5[p]*(cost_2-cost_1)+w10[p]*(cost_3-cost_2)));


//Constraints
subject to{

  //each providers provides 0% or 50% or 100% of the available workers + extra
  forall (p in P)
   	w[p] == (a[p]*available_workers[p]+ex[p])+(h[p]*0.5*available_workers[p]);

  //ensure that we only can get extra workers when we alredy get al the workers of a determinated provider
  forall (p in P)
   	ex[p] <= available_workers[p]*a[p];

  //we just can get all or the half or the 0 but not all of them
  forall (p in P)
   	h[p]+a[p] <= 1;

  //there can't be two providers form the same country
  forall(p1 in P, p2 in P:p1 < p2 && country[p1]==country[p2])
	h[p1]+a[p1]+h[p2]+a[p2]<=1;

  // the sum of all the workers provided by the providers must be equal to the workers requested
  sum (p in P) w[p] == wr;

  //count the number of workers greater than 5
  forall (p in P){
   	w[p]-5<=w5[p];
   	w5[p]>=0;
  }

  //count the number of workers greater than 10
  forall (p in P){
   	w[p]-10<=w10[p];
   	w10[p]>=0;
  }

  //ensure that all variables are positive
  forall (p in P){
    w[p] >= 0;
   	ex[p] >= 0;
   	h[p] >= 0;
   	a[p] >= 0;
   	w5[p] >= 0;
   	w10[p] >= 0;
  }
}

//Post processing data
execute {
 	writeln("In order to hire "+wr+" at the minimum cost the best providers are:");\
 	writeln(w)
  	for (var p in P)
  		if (w[p] >=1) writeln("provider "+ p +" from the country " + country[p] + " with " + w[p] + " workers, from which  "+ex[p]+"  are extra workers");
 } 
