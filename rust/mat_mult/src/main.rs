extern crate rand;
extern crate matrix;

use rand::Rng;
use matrix::prelude::*;


use std::thread;
use std::collections::HashMap;
use std::env;
use std::process::exit;
use std::time::{Duration,Instant};

#[derive(Clone)]
struct Algorithm{
	mult_algo: HashMap<String, String>,
	int_maps: Vec<HashMap<String, i32>>,
	h_term_lists: HashMap<String, Vec<String>>,
	c_term_lists: HashMap<String, Vec<String>>,
	solo_h_list_a: Vec<String>,
	solo_h_list_b: Vec<String>,
	solo_c_list: Vec<String>,
	fitness_cells: u32,
	fitness_difference: u32,
}

struct MatMult{
	mat_triples: Vec<(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)>,
	mat_size: (usize,usize),
	start_terms: usize,
	num_triples: usize,
	SMALL: u32,
	MEDIUM: u32,
	LARGE: u32,
	num_terms: usize,
	verbose: bool,
	cells_priority: bool,
	h_added: u32,
}

fn init_mats(mut mat_trips: &mut Vec<(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)>, num_triples: usize, mat_size: (usize, usize)){

	let mat_x: usize = mat_size.0;
	let mat_y: usize = mat_size.1;
	
	let mut rng = rand::thread_rng();
	let z: i32 = rng.gen_range(-10..11);
	
	let mut m1: matrix::prelude::Compressed<i32> = Compressed::zero((5,5));
	let mut m2: matrix::prelude::Compressed<i32> = Compressed::zero((5,5));
	let mut m3: matrix::prelude::Compressed<i32> = Compressed::zero((5,5));
	
	for triple in 0..num_triples{
	
		for x in 0..mat_x{
			for y in 0..mat_y{
			
				m1.set((x,y), rng.gen_range(-10..11));
				m2.set((x,y), rng.gen_range(-10..11));
			}	
		}
	
		for x in 0..mat_x{
			for y in 0..mat_x{
			
				let mut current = 0;
				
				for z in 0..mat_y{
					
					current += m1.get((x,z)) * m2.get((z,y));
				}
				m3.set((x,y), current);
			}	
		}
		mat_trips.push((m1.clone(),m2.clone(),m3.clone()));
	}
}	

fn eval_single_c(int_map: &mut HashMap<String, i32>, c_list: Vec<String>, c_key: String){
	
	let mut res = 0;
	let mut h_int_vec = [].to_vec();
				
	for term in c_list{ //Iterate through each h-term in the c-term
				
		let mut read_term = term.clone();
		let mut negative = false;
					
		if read_term.contains("-") { negative = true }
					
		read_term = read_term.replace(" - ", "");
					
		if negative{
			h_int_vec.push(int_map[&read_term] - 2*int_map[&read_term])
		} else {
			h_int_vec.push(int_map[&read_term])
		}	
	}
	res = h_int_vec.iter().sum();
	int_map.insert(c_key, res);	
		
}

fn eval_single_h(int_map: &mut HashMap<String, i32>, h_list: Vec<String>, h_key: String, mat_triple: (matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)){

	let mut res = 0;
	let now = Instant::now();
	let mut a_res = 0;
	let mut b_res = 0;
						
	let mut a_vec = [].to_vec();
	let mut a_int_vec: Vec<i32> = [].to_vec();
	let mut b_vec = [].to_vec();
	let mut b_int_vec:  Vec<i32>  = [].to_vec();
					
	for term in h_list{ //Iterate through all terms in the equation and replace with corresponding int
					
		let mut negative = false;
		let mut read_term = term.clone();
						
		if term.contains("-"){ negative = true; }
					
		read_term = read_term.replace(" - ", "");
		let x_coord = read_term[1..2].to_string().parse::<usize>().unwrap()-1;
		let y_coord = read_term[2..3].to_string().parse::<usize>().unwrap()-1;
						
		if term.contains("a"){ 
			a_vec.push(read_term);
			if negative{
				a_int_vec.push( (mat_triple.0.get((x_coord, y_coord))) - (2*(mat_triple.0.get((x_coord, y_coord)))))
			} else {
				a_int_vec.push( mat_triple.0.get((x_coord, y_coord)))
			}
		} else if term.contains("b"){ 
			b_vec.push(read_term);

			if negative{
				b_int_vec.push( (mat_triple.1.get((x_coord, y_coord))) - (2*(mat_triple.1.get((x_coord, y_coord)))))
			} else {
				b_int_vec.push( mat_triple.1.get((x_coord, y_coord)))
			}
		}
	}
	a_res = a_int_vec.iter().sum();
	b_res = b_int_vec.iter().sum();
	int_map.insert(h_key.clone(), a_res*b_res);
}

fn init_maps(mut algo: &mut Algorithm, new_algo: &Algorithm, matmult: &MatMult, mat_triples: &Vec<(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)>, num_terms: usize, term_size: u32, mat_size: (usize, usize)){

	let mat_triples = &matmult.mat_triples;
	
	for mat_triple in 0..mat_triples.len() {
	
		let mut int_map: HashMap<String, i32> = HashMap::new();
		algo.int_maps.push(int_map);

		for h in algo.h_term_lists.keys(){ //Iterate through all h-terms
				
			eval_single_h(&mut algo.int_maps[mat_triple], algo.h_term_lists[h].clone(), h.to_string(), mat_triples[mat_triple].clone());
		}
		
		for c in algo.c_term_lists.keys(){
			
				eval_single_c(&mut algo.int_maps[mat_triple], algo.c_term_lists[c].clone(), c.to_string());
		}
		
	}
	
}


fn update_maps(algo: &mut Algorithm, new_algo: &Algorithm, mat_triples: &Vec<(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)>, num_terms: usize, term_size: u32, mat_size: (usize, usize), mutation_type: usize, keys: Vec<String>){

	for mat_triple in 0..mat_triples.len(){
	
		for key in &keys{
		
			if key.contains("h"){
			
				eval_single_h(&mut algo.int_maps[mat_triple], algo.h_term_lists[key].clone(), key.to_string(), mat_triples[mat_triple].clone());
			
			} else if key.contains("c"){
			
				eval_single_c(&mut algo.int_maps[mat_triple], algo.c_term_lists[key].clone(), key.to_string());
			
			}
		
		}
	
	}
	
	
	
}

fn get_fitness(mut algo: &mut Algorithm, new_algo: &Algorithm, matmult: &MatMult, mat_triples: &Vec<(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)>, num_terms: usize, term_size: u32, mat_size: (usize, usize),mutation_type: usize, no_mutate: bool) -> (i32, usize){

	let mut fitness_difference = 0;
	let mut fitness_difference_final = 0;
	let mut fitness_cells = 0;
	let mut res_map: HashMap<String, i32> = HashMap::new();
	let mut mat_triples = &matmult.mat_triples;
	let mut num_terms = matmult.num_terms;
	let mut term_size = matmult.MEDIUM;
	let mut mat_size = matmult.mat_size;
	
	for x in 0..mat_triples.len(){	//Iterate though each matrix triple
		
		for row in 1..mat_size.0+1{
			for col in 1..mat_size.1+1{	//Iterate through each c-term
			
				fitness_difference = 0;
			
				let mut current_c = String::from("c");
				current_c.push_str(row.to_string().as_str());
				current_c.push_str(col.to_string().as_str());
				
				let res = algo.int_maps[x][&current_c];
				
				if res != mat_triples[x].2.get((row-1, col-1)){

					fitness_difference += (mat_triples[x].2.get((row-1,col-1)) - res).abs();
					fitness_cells += 1
				}
			}
		}	
		fitness_difference /= 25;
		fitness_difference_final += fitness_difference;
	}
	fitness_cells /= mat_triples.len();
	
	(fitness_difference_final, fitness_cells)

}

fn print_mats(mat_trip: &(matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>,matrix::prelude::Compressed<i32>)){

	for x in 0..5{
		println!("{} {} {} {} {}", mat_trip.0.get((x,0)), mat_trip.0.get((x,1)), mat_trip.0.get((x,2)), mat_trip.0.get((x,3)), mat_trip.0.get((x,4)))
	}
	println!("\n");
	for x in 0..5{
		println!("{} {} {} {} {}", mat_trip.1.get((x,0)), mat_trip.1.get((x,1)), mat_trip.1.get((x,2)), mat_trip.1.get((x,3)), mat_trip.1.get((x,4)))
	}
	println!("\n");
	for x in 0..5{
		println!("{} {} {} {} {}", mat_trip.2.get((x,0)), mat_trip.2.get((x,1)), mat_trip.2.get((x,2)), mat_trip.2.get((x,3)), mat_trip.2.get((x,4)))
	}
	println!("\n");
}

fn rand_algo(term_size: u32, num_terms: usize, mat_size: (usize, usize)) -> Algorithm{

	let mut algo = Algorithm{
		mult_algo: HashMap::new(),
		h_term_lists: HashMap::new(),
		c_term_lists: HashMap::new(),
		int_maps: [].to_vec(),
		solo_h_list_a: [].to_vec(),
		solo_h_list_b: [].to_vec(),
		solo_c_list: [].to_vec(),
		fitness_cells: 1000,
		fitness_difference: 1000,
	};
	
	for x in 1..num_terms+1{
	
		let mut h_term_list = make_h_list(term_size);
		let mut h_term = make_h(&h_term_list);
		let mut h_term_name = String::from("h");
		h_term_name.push_str(x.to_string().as_str());
		
		algo.h_term_lists.insert(h_term_name.clone(), h_term_list);
		algo.mult_algo.insert(h_term_name, h_term);
	}
	
	for x in 1..mat_size.0+1{
		for y in 1..mat_size.1+1{
			
			let mut c_term_list = make_c_list(term_size, num_terms);
			
			let mut c_term = make_c(&c_term_list);
			let mut c_term_name = String::from("c");
			
			
			c_term_name.push_str(x.to_string().as_str());
			c_term_name.push_str(y.to_string().as_str());
			
			algo.c_term_lists.insert(c_term_name.clone(), c_term_list);
			algo.mult_algo.insert(c_term_name, c_term);
			
		}
	}
	
	algo
}

fn print_algo(algo: &Algorithm, num_terms: usize, mat_size: (usize, usize)){

	println!("NUMTERMS: {}", num_terms);

	for x in 1..num_terms+1{
	
		let mut term_name = String::from("h");
		term_name.push_str(x.to_string().as_str());
		if algo.mult_algo.contains_key(&term_name){
			println!("{}: {}", term_name, algo.mult_algo[&term_name]);
		}
	}
	
	println!("\n");
	
	for x in 1..mat_size.0+1{
		for y in 1..mat_size.1+1{
		
				let mut term_name = String::from("c");
				term_name.push_str(x.to_string().as_str());
				term_name.push_str(y.to_string().as_str());
				
				println!("{}: {}", term_name, algo.mult_algo[&term_name]);
		
		}
	}

}

fn make_ab_term(term_size: u32) -> String{
	
	let mut rng = rand::thread_rng();
	let z: i32 = rng.gen_range(0..2);
	
	let mut term = String::from("");
	
	if z == 0{
		term.push_str(" - ");	
	}
	
	let z: i32 = rng.gen_range(0..2);
	
	if z == 0{ term.push('a') } else { term.push('b') }
	
	let z: i32 = rng.gen_range(1..6);
	
	term.push_str(z.to_string().as_str());
	
	let z: i32 = rng.gen_range(1..6);
	
	term.push_str(z.to_string().as_str());
	
	term
	
}

fn make_h_list(term_size: u32) -> Vec<String>{

	let mut h_term_list: Vec<String> = [].to_vec();
	
	for x in 0..term_size{
		h_term_list.push(make_ab_term(term_size));
	}

	
	if one_sided_h(&h_term_list){
		h_term_list = make_h_list(term_size);
	}

	h_term_list

}

fn make_h(h_term_list: &Vec<String>) -> String{

	let mut h_term_a = String::from("");
	let mut h_term_b = String::from("");

	for x in 0..h_term_list.len(){
		if h_term_list[x].contains("a") && !h_term_list[x].contains("-"){
			h_term_a.push_str(" + ");
			h_term_a.push_str(h_term_list[x].as_str())
		}
	}
	
	for x in 0..h_term_list.len(){
		if h_term_list[x].contains("a") && h_term_list[x].contains("-"){
			h_term_a.push_str(h_term_list[x].as_str())
		}
	}
	
	for x in 0..h_term_list.len(){
		if h_term_list[x].contains("b") && !h_term_list[x].contains("-"){
			h_term_b.push_str(" + ");
			h_term_b.push_str(h_term_list[x].as_str())
		}
	}
	for x in 0..h_term_list.len(){
		if h_term_list[x].contains("b") && h_term_list[x].contains("-"){
			h_term_b.push_str(h_term_list[x].as_str());
		}
	}
	
	h_term_a = h_term_a.trim().to_string();
	h_term_b = h_term_b.trim().to_string();
	if h_term_a.as_bytes()[0] as char == '+' {h_term_a = h_term_a[1..h_term_a.len()].to_string()}
	if h_term_b.as_bytes()[0] as char == '+' {h_term_b = h_term_b[1..h_term_b.len()].to_string()}
	h_term_a = h_term_a.trim().to_string();
	h_term_b = h_term_b.trim().to_string();
	let mut temp = String::from('('); temp.push_str(h_term_a.as_str()); temp.push(')'); h_term_a = temp;
	let mut temp = String::from('('); temp.push_str(h_term_b.as_str()); temp.push(')'); h_term_b = temp;
	if h_term_a.as_bytes()[2] as char == ' ' {h_term_a = h_term_a.replacen(" ", "", 1)}
	if h_term_b.as_bytes()[2] as char == ' ' {h_term_b = h_term_b.replacen(" ", "", 1)}
	
	let mut h_term = String::from(h_term_a);
	h_term.push_str(" * ");
	h_term.push_str(h_term_b.as_str()); 
	
	h_term
	
}

fn make_c_list(term_size: u32, num_terms: usize) -> Vec<String>{

	let mut c_term_list: Vec<String> = [].to_vec();
	
	let mut rng = rand::thread_rng();

	for x in 0..term_size{
	
		let z: i32 = rng.gen_range(0..2);
		let mut term = String::from("");
		
		if z == 0{ term.push_str(" - ")}
		term.push('h');
		
		let z: usize = rng.gen_range(1..num_terms+1);
		term.push_str(z.to_string().as_str());
		
		c_term_list.push(term);
	}
		
	c_term_list

}

fn make_c(c_term_list: &Vec<String>) -> String{

	let mut c_term = String::from("");
	
	for x in 0..c_term_list.len(){
		if !c_term_list[x].contains("-"){
			c_term.push_str(" + ");
			c_term.push_str(c_term_list[x].as_str())
		}
	}
	
	for x in 0..c_term_list.len(){
		if c_term_list[x].contains("-"){
			c_term.push_str(c_term_list[x].as_str())
		}
	}
	
	c_term = c_term.trim().to_string();
	//println!("Here is the error: {:?}", c_term_list);
	if c_term.as_bytes()[0] as char == '+'{c_term = c_term[1..c_term.len()].to_string()}
	c_term = c_term.trim().to_string();
	c_term.push(' ');
	if c_term.as_bytes()[0] as char == ' '{c_term = c_term.replacen(" ", "", 1)}
	
	c_term

}

fn one_sided_h(h_term_list: &Vec<String>) -> bool{

	let mut num_a = 0;
	let mut num_b = 0;
	
	for x in 0..h_term_list.len(){

		if h_term_list[x].contains("a"){ num_a += 1} else if h_term_list[x].contains("b"){num_b +=1}
	}
	
	if num_a == 0 || num_b == 0 {return true;} 
	
	false

}

fn mutate(mut algo: &mut Algorithm, term_size: u32, mut num_terms: usize, mat_size: (usize, usize), num_triples: usize) -> (&Algorithm, usize, usize, bool, Vec<String>){

	/*
	
	Mutation types:
	1: Add h
	2: Remove h
	3: Add (+/-)a to h
	4: Add (+/-)b to h
	5: Remove a from h
	6: Remove b from h
	7: Add (+/-)h to c
	8: Remove h from c
	
	*/
	
	let mut rng = rand::thread_rng();
	//let mut mutation_type: usize = 8;
	let mut mutation_type: usize = rng.gen_range(1..9);
	println!("MUT {}", mutation_type);
	let mut no_mutate: bool = false;
	let mut keys = [].to_vec();
	
	if mutation_type == 1{

		let mut h_to_add = String::from("h");
		h_to_add.push_str((num_terms+1).to_string().as_str());
		
		keys.push(h_to_add.clone());
		
		let mut new_h_list = make_h_list(term_size);
		let mut new_h = make_h(&new_h_list);
		
		algo.h_term_lists.insert(h_to_add.clone(), new_h_list);
		algo.mult_algo.insert(h_to_add.clone(), new_h);
		
		//Also add this new h to one of the c's
		
		let mut row: usize = rng.gen_range(1..6);
		let mut col: usize = rng.gen_range(1..6);
		
		let mut c_to_add_to = String::from("c");
		c_to_add_to.push_str(row.to_string().as_str());
		c_to_add_to.push_str(col.to_string().as_str());
		
		let mut random: usize = rng.gen_range(0..2);
		let mut new_h_name = String::from(" - "); 
		
		keys.push(c_to_add_to.clone());
		
		if random == 0{ new_h_name.push_str(h_to_add.as_str()); h_to_add = new_h_name.clone();}
		
		//println!("Adding {}", h_to_add);
		
		algo.c_term_lists.get_mut(&c_to_add_to).map(|val| val.push(h_to_add));
		algo.mult_algo.insert(c_to_add_to.clone(), make_c(&algo.c_term_lists[&c_to_add_to]));
		
		num_terms += 1;
		
	} else if mutation_type == 2{
	
		let mut unremovable_list: Vec<String> = [].to_vec();
		let mut used_h_list: Vec<String> = [].to_vec();
		
		//println!("MUT 2");
		
		for row in 1..(mat_size.0)+1{
			for col in 1..(mat_size.1)+1{
				let mut current_c = String::from("c");
				current_c.push_str(row.to_string().as_str());
				current_c.push_str(col.to_string().as_str());
				for h in &algo.c_term_lists[&current_c]{ if !used_h_list.contains(&h){ used_h_list.push(h.to_string())}}
				if algo.c_term_lists[&current_c].len() == 1{
					if algo.c_term_lists[&current_c][0].contains("-") && !unremovable_list.contains(&algo.c_term_lists[&current_c][0][3..].to_string()){
						unremovable_list.push(algo.c_term_lists[&current_c][0][3..].to_string());
						//println!("{} is unremovable because of {:?}", algo.c_term_lists[&current_c][0], algo.c_term_lists[&current_c]);
					} else if !algo.c_term_lists[&current_c][0].contains("-") && !unremovable_list.contains(&algo.c_term_lists[&current_c][0]){
						unremovable_list.push(algo.c_term_lists[&current_c][0].clone());
						//println!("{} is unremovable because of {:?}", algo.c_term_lists[&current_c][0], algo.c_term_lists[&current_c]);
					}
				} else {
				
					let mut count = 0;
					
					let mut h = &algo.c_term_lists[&current_c][0].replace(" - ", "");
					let mut neg_check = String::from(" - ");
					neg_check.push_str(h.as_str());
					
					for x in 0..algo.c_term_lists[&current_c].len(){
						
						if &algo.c_term_lists[&current_c][x] == h || algo.c_term_lists[&current_c][x] == neg_check{count +=1}
					}
					
					if count == algo.c_term_lists[&current_c].len() && !unremovable_list.contains(h){ unremovable_list.push(h.to_string()); /*println!("{} is unremovable because of {:?}", algo.c_term_lists[&current_c][0], algo.c_term_lists[&current_c]);*/}
					
					//println!("for {}, length is {}, count is {}", h, algo.c_term_lists[&current_c].len(), count );
					//println!("heres the list: {:?}", algo.c_term_lists[&current_c]);
				}
			}
		}
		
		let mut term_index = rng.gen_range(0..algo.h_term_lists.keys().len());
		let keys1: Vec<&str> = algo.h_term_lists.keys().map(|k| k.as_str()).collect();
		let mut h_to_remove = keys1[term_index].to_string();
		
		while !algo.mult_algo.contains_key(&h_to_remove) || unremovable_list.contains(&h_to_remove){
			
			if unremovable_list.len() == keys.len(){
				no_mutate = true;
				println!("No mutate1");
				return (algo, num_terms, mutation_type,  no_mutate, keys)
			}	
			//if unremovable_list.contains(&h_to_remove){ println!("UNREMOVABLE: {} \n, key {:?} \n, unremovable {:?}", h_to_remove, keys, unremovable_list); }

			term_index = rng.gen_range(0..algo.h_term_lists.keys().len());
			h_to_remove = keys1[term_index].to_string();
			

		}		
		
		for x in 0..num_triples{
			algo.int_maps[x].remove(&h_to_remove);
		}
		
		algo.mult_algo.remove(&h_to_remove);
		algo.h_term_lists.remove(&h_to_remove);
		if algo.solo_h_list_a.contains(&h_to_remove){
			let mut index = algo.solo_h_list_a.iter().position(|x| *x == h_to_remove).unwrap();
			algo.solo_h_list_a.remove(index);
		}
		if algo.solo_h_list_b.contains(&h_to_remove){
			let mut index = algo.solo_h_list_b.iter().position(|x| *x == h_to_remove).unwrap();
			algo.solo_h_list_b.remove(index);
		}
		
		for row in 1..(mat_size.0)+1{
			for col in 1..(mat_size.1)+1{
				let mut current_c = String::from("c");
				current_c.push_str(row.to_string().as_str());
				current_c.push_str(col.to_string().as_str());
				let mut neg_check = String::from(" - ");
				neg_check.push_str(h_to_remove.as_str());
				
				if algo.c_term_lists[&current_c].contains(&h_to_remove){
					//println!("Removing {} from {}: {:?}", &h_to_remove, &current_c, algo.c_term_lists[&current_c]);
					//println!("{:?}", algo.c_term_lists[&current_c]);
					keys.push(current_c.clone());
						
					while algo.c_term_lists[&current_c].contains(&h_to_remove){
						let mut index = algo.c_term_lists[&current_c].iter().position(|x| *x == h_to_remove).unwrap();
						algo.c_term_lists.get_mut(&current_c).map(|val| val.remove(index));
					}
					algo.mult_algo.insert(current_c.clone(), make_c(&algo.c_term_lists[&current_c]));
				}
				
				if algo.c_term_lists[&current_c].contains(&neg_check){
					//println!("Removing from {}", &current_c);
					keys.push(current_c.clone());
					
					while algo.c_term_lists[&current_c].contains(&neg_check){
					
						let mut index = algo.c_term_lists[&current_c].iter().position(|x| *x == neg_check).unwrap();
						algo.c_term_lists.get_mut(&current_c).map(|val| val.remove(index));

					}
					algo.mult_algo.insert(current_c.clone(), make_c(&algo.c_term_lists[&current_c]));
				}
			}
		}
	} else if mutation_type == 3{
	
		let mut random = rng.gen_range(0..2);
		let mut a_to_add = String::from("");
		
		if random == 0{ a_to_add.push_str(" - ")}
		a_to_add.push('a');
		
		let mut row = rng.gen_range(1..6);
		let mut col = rng.gen_range(1..6);
		
		a_to_add.push_str(row.to_string().as_str());
		a_to_add.push_str(col.to_string().as_str());
		
		let mut h_no = rng.gen_range(1..num_terms+1);
	
		let mut h_to_add_to = String::from("h");
		h_to_add_to.push_str(h_no.to_string().as_str());
		
		while !algo.mult_algo.contains_key(&h_to_add_to){
			let mut h_no = rng.gen_range(1..num_terms+1);
	
			h_to_add_to = String::from("h");
			h_to_add_to.push_str(h_no.to_string().as_str());
		}
		
		//println!("ADDING {} TO: {}", a_to_add, h_to_add_to);
		
		keys.push(h_to_add_to.clone());
		
		algo.h_term_lists.get_mut(&h_to_add_to).map(|val| val.push(a_to_add));
		
		algo.mult_algo.insert(h_to_add_to.clone(), make_h(&algo.h_term_lists[&h_to_add_to]));
		
		if algo.solo_h_list_a.contains(&h_to_add_to){
			let mut index = algo.solo_h_list_a.iter().position(|x| *x == h_to_add_to).unwrap();
			algo.solo_h_list_a.remove(index);
		}
	
	} else if mutation_type == 4{
	
		let mut random = rng.gen_range(0..2);
		let mut b_to_add = String::from("");
		
		if random == 0{ b_to_add.push_str(" - ")}
		b_to_add.push('b');
		
		let mut row = rng.gen_range(1..6);
		let mut col = rng.gen_range(1..6);
		
		b_to_add.push_str(row.to_string().as_str());
		b_to_add.push_str(col.to_string().as_str());
		
		let mut h_no = rng.gen_range(1..num_terms+1);
	
		let mut h_to_add_to = String::from("h");
		h_to_add_to.push_str(h_no.to_string().as_str());
		
		while !algo.mult_algo.contains_key(&h_to_add_to){
			let mut h_no = rng.gen_range(1..num_terms+1);
	
			h_to_add_to = String::from("h");
			h_to_add_to.push_str(h_no.to_string().as_str());
		}
		
		//println!("ADDING {} TO: {}", b_to_add, h_to_add_to);
		keys.push(h_to_add_to.clone());
		
		algo.h_term_lists.get_mut(&h_to_add_to).map(|val| val.push(b_to_add));
		
		algo.mult_algo.insert(h_to_add_to.clone(), make_h(&algo.h_term_lists[&h_to_add_to]));
		
		if algo.solo_h_list_b.contains(&h_to_add_to){
			let mut index = algo.solo_h_list_b.iter().position(|x| *x == h_to_add_to).unwrap();
			algo.solo_h_list_b.remove(index);
		}
	
	} else if mutation_type == 5{
	
		let mut h_to_remove_from = String::from("");
		let mut valid = false;
		
		while !valid{
		
			h_to_remove_from.push('h');
			let mut h_no = rng.gen_range(1..num_terms+1);
			h_to_remove_from.push_str(h_no.to_string().as_str());
			
			while !algo.mult_algo.contains_key(&h_to_remove_from){
				h_to_remove_from = String::from("h");
				let mut h_no = rng.gen_range(1..num_terms+1);
				h_to_remove_from.push_str(h_no.to_string().as_str());
			}
			
			let mut num_a = 0;
		
			for term in 0..algo.h_term_lists[&h_to_remove_from].len(){
			
				if algo.h_term_lists[&h_to_remove_from][term].contains("a"){
					num_a +=1;
					
				}
				
				if num_a > 1{
					valid = true;
				} else if !algo.solo_h_list_a.contains(&h_to_remove_from){
					algo.solo_h_list_a.push(h_to_remove_from.clone());
				}
				
				if algo.solo_h_list_a.len() == algo.h_term_lists.keys().len(){
					no_mutate = true;
					println!("No mutate2");
					return (algo, num_terms, mutation_type, no_mutate, keys)
				}
			
			}
		
		}
		
		keys.push(h_to_remove_from.clone());
		
		let mut a_terms = [].to_vec();
		
		for x in 0..algo.h_term_lists[&h_to_remove_from].len(){
		
			if algo.h_term_lists[&h_to_remove_from][x].contains("a"){
				a_terms.push(&algo.h_term_lists[&h_to_remove_from][x]);
			}
		}
		
		let mut picked_term_i = rng.gen_range(0..a_terms.len());
		let mut picked_term = String::from(a_terms[picked_term_i]);
		
		//println!("REMOVING {} FROM {}", picked_term, h_to_remove_from);
		
		let mut index = algo.h_term_lists[&h_to_remove_from].iter().position(|x| *x == picked_term).unwrap();
		algo.h_term_lists.get_mut(&h_to_remove_from).map(|val| val.remove(index));
		
		algo.mult_algo.insert(h_to_remove_from.clone(), make_h(&algo.h_term_lists[&h_to_remove_from]));
		
	} else if mutation_type == 6{
	
		let mut h_to_remove_from = String::from("");
		let mut valid = false;
		
		while !valid{
		
			h_to_remove_from.push('h');
			let mut h_no = rng.gen_range(1..num_terms+1);
			h_to_remove_from.push_str(h_no.to_string().as_str());
			
			while !algo.mult_algo.contains_key(&h_to_remove_from){
				h_to_remove_from = String::from("h");
				let mut h_no = rng.gen_range(1..num_terms+1);
				h_to_remove_from.push_str(h_no.to_string().as_str());
			}
			
			let mut num_b = 0;
		
			for term in 0..algo.h_term_lists[&h_to_remove_from].len(){
			
				if algo.h_term_lists[&h_to_remove_from][term].contains("b"){
					num_b +=1;
					
				}
				
				if num_b > 1{
					valid = true;
				} else if !algo.solo_h_list_b.contains(&h_to_remove_from){
					algo.solo_h_list_b.push(h_to_remove_from.clone());
				}
				
				if algo.solo_h_list_b.len() == algo.h_term_lists.keys().len(){
					no_mutate = true;
					println!("No mutate3");
					return (algo, num_terms, mutation_type, no_mutate, keys)
				}
			
			}
		
		}
	
		keys.push(h_to_remove_from.clone());
		
		let mut b_terms = [].to_vec();
		
		for x in 0..algo.h_term_lists[&h_to_remove_from].len(){
		
			if algo.h_term_lists[&h_to_remove_from][x].contains("b"){
				b_terms.push(&algo.h_term_lists[&h_to_remove_from][x]);
			}
		}
		
		let mut picked_term_i = rng.gen_range(0..b_terms.len());
		let mut picked_term = String::from(b_terms[picked_term_i]);
		
		//println!("REMOVING {} FROM {}", picked_term, h_to_remove_from);
		
		let mut index = algo.h_term_lists[&h_to_remove_from].iter().position(|x| *x == picked_term).unwrap();
		algo.h_term_lists.get_mut(&h_to_remove_from).map(|val| val.remove(index));
		
		algo.mult_algo.insert(h_to_remove_from.clone(), make_h(&algo.h_term_lists[&h_to_remove_from]));	
	
	} else if mutation_type == 7{
	
		let mut h_no = rng.gen_range(1..num_terms+1);
		
		let mut rand = rng.gen_range(0..2);
		let mut h_to_add = String::from("");
		if rand == 0{ h_to_add.push('h') } else { h_to_add.push_str(" - h") }

		h_to_add.push_str(h_no.to_string().as_str());

		
		while !algo.mult_algo.contains_key(&h_to_add){
			h_no = rng.gen_range(1..num_terms+1);
			h_to_add = String::from("h");
			h_to_add.push_str(h_no.to_string().as_str());
		}
		
		
		
		let mut row = rng.gen_range(1..(mat_size.0)+1);
		let mut col = rng.gen_range(1..(mat_size.1)+1);
		let mut c_to_add_to = String::from("c");
		
		c_to_add_to.push_str(row.to_string().as_str());
		c_to_add_to.push_str(col.to_string().as_str());
		
		keys.push(c_to_add_to.clone());
		
		//println!("Adding {} to {}", h_to_add, c_to_add_to);
		
		algo.c_term_lists.get_mut(&c_to_add_to).map(|val| val.push(h_to_add));
		algo.mult_algo.insert(c_to_add_to.clone(), make_c(&algo.c_term_lists[&c_to_add_to]));
		
	
	} else if mutation_type == 8{
	
	let mut c_to_remove_from = String::from("c");
	let mut valid = false;
	
	while !valid{
	
		c_to_remove_from = String::from("c");
		let mut row = rng.gen_range(1..(mat_size.0)+1);
		let mut col = rng.gen_range(1..(mat_size.1)+1); 
		c_to_remove_from.push_str(row.to_string().as_str());
		c_to_remove_from.push_str(col.to_string().as_str());
		
		if algo.c_term_lists[&c_to_remove_from].len() > 1{
			valid = true;
		} else if !algo.solo_c_list.contains(&c_to_remove_from){
			algo.solo_c_list.push(c_to_remove_from.clone());
		}
		
		if algo.solo_c_list.len() == algo.c_term_lists.keys().len(){
			no_mutate = true;
			println!("No mutate4");
			print_algo(&algo, num_terms, mat_size);
			println!("solo_c_list: {:?}", algo.solo_c_list);
			exit(0x0100);
			return (algo, num_terms, mutation_type, no_mutate, keys)
		}
	
	}
	
	keys.push(c_to_remove_from.clone());

	let mut picked_term_i = rng.gen_range(0..algo.c_term_lists[&c_to_remove_from].len());
	let mut picked_term = &algo.c_term_lists[&c_to_remove_from][picked_term_i];
	
	//println!("Removing {} from {}", picked_term, c_to_remove_from);
	
	let mut index = algo.c_term_lists[&c_to_remove_from].iter().position(|x| x == picked_term).unwrap();
	algo.c_term_lists.get_mut(&c_to_remove_from).map(|val| val.remove(index));
	
	algo.mult_algo.insert(c_to_remove_from.clone(), make_c(&algo.c_term_lists[&c_to_remove_from]));
	
	}
	
	(algo, num_terms, mutation_type, no_mutate, keys)

}

fn main() {
	let args: Vec<String> = env::args().collect();
	
	if args.len() < 2 {
		println!("Not enough arguments given, please try again.");
		exit(0x0100);
	}
	
	let num_triples = &args[1];

	let mut Matmult = MatMult {
		mat_triples: [].to_vec(),
		mat_size: (5,5),
		start_terms: 0, //Init to 125
		num_triples: 5,
		SMALL: 2,
		MEDIUM: 5,
		LARGE: 10,
		num_terms: 0, //Init to start_terms
		verbose: false,
		cells_priority: false,
		h_added: 0,		
	};
	
	Matmult.start_terms = Matmult.mat_size.0 * Matmult.mat_size.0 * Matmult.mat_size.1; // Init start_terms
	Matmult.num_terms = Matmult.start_terms; 					    // Init num_terms
	Matmult.num_triples = 30;							    // Init num_triples	
	
	init_mats(&mut Matmult.mat_triples, Matmult.num_triples, Matmult.mat_size);
	let mut algo = rand_algo(Matmult.MEDIUM, Matmult.num_terms, Matmult.mat_size);
	let mut new_algo = algo.clone();
	let (mut fitness_difference, mut fitness_cells) = (0,0);
	let now = Instant::now();
	init_maps(&mut algo, &new_algo, &Matmult, &Matmult.mat_triples, Matmult.num_terms, Matmult.MEDIUM, Matmult.mat_size);
	let now2 = Instant::now();
	println!("Time to init: {:?}", now2.duration_since(now));
	let now = Instant::now();
	for x in 0..10000{
	
		
		
		//(fitness_difference, fitness_cells) = get_fitness(&mut algo, &new_algo, &Matmult, &Matmult.mat_triples, Matmult.num_terms, Matmult.MEDIUM, Matmult.mat_size, 0, false);

		if x % 100 == 0 {println!("Mutation {}", x); }
		let res = mutate(&mut algo, Matmult.MEDIUM, Matmult.num_terms, Matmult.mat_size, Matmult.num_triples);
		Matmult.num_terms = res.1;
		let mut no_mutate = res.3.clone();
		let mut mutation_type = res.2.clone();
		let mut keys = res.4.clone();
		
		let now = Instant::now();
		update_maps(&mut algo, &new_algo, &Matmult.mat_triples, Matmult.num_terms, Matmult.MEDIUM, Matmult.mat_size, mutation_type, keys);
		let now2 = Instant::now();
		
		//thread::sleep_ms(1000);
		
		//println!("Time2: {:?}", now2.duration_since(now));
		(fitness_difference, fitness_cells) = get_fitness(&mut algo, &new_algo, &Matmult, &Matmult.mat_triples, Matmult.num_terms, Matmult.MEDIUM, Matmult.mat_size, mutation_type, no_mutate);

	}
	print_algo(&algo, Matmult.num_terms, Matmult.mat_size);
	
	let now2 = Instant::now();
	println!("Time to run: {:?}", now2.duration_since(now));
	println!("fit_diff {}", fitness_difference);
	println!("fit_cells {}", fitness_cells);


	let mut Hashtest = HashMap::new();
	
	Hashtest.insert("a",1);
	Hashtest.insert("b",2);
	Hashtest.insert("c",3);
	
	for value in Hashtest.values(){
		println!("Value: {}", value);
	}
} 
