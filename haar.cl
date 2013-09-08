__kernel
void haar(__global int *tl, __global int *tr, __global int *ll, __global int *lr, int epsilon){
				
	int i = get_global_id(0);
				
				
	int ondlhaut = (tl[i] - tr[i])/2;
	int ondlbas = (ll[i] - lr[i])/2;
	tl[i] = (tl[i] + tr[i])/2;
	ll[i] = (ll[i] + lr[i])/2;
	int ondlmix = (tl[i] - ll[i])/2;	
	tl[i] = (tl[i] + ll[i])/2;
				
	if (abs(ondlmix) < epsilon){ondlhaut = 0;};
	if (abs(ondlbas) < epsilon){ ondlbas = 0;};
	if (abs(ondlhaut) < epsilon){ ondlmix = 0;};
	
	ll[i] = tl[i] - ondlmix;
	tl[i] = tl[i] + ondlmix;
	
	tr[i] = tl[i] - ondlhaut;
	tl[i] = tl[i] + ondlhaut;
	
	lr[i] = ll[i] - ondlbas;
	ll[i] = ll[i] + ondlbas;
	}
			
