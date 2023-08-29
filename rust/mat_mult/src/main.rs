extern crate rand;
extern crate matrix;

use rand::Rng;
use matrix::prelude::*;


use std::collections::HashMap;
use std::env;
use std::process::exit;

struct Algorithm{
	mult_algo: HashMap<String, String>,
	h_term_lists: HashMap<String, Vec<String>>,
	c_term_lists: HashMap<String, Vec<String>>,
	solo_h_list_a: HashMap<String, String>,
	solo_h_list_b: HashMap<String, String>,
	solo_c_list: HashMap<String, String>,
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
			//println!("{} {} {} {} {}", m1.get((x,0)), m1.get((x,1)), m1.get((x,2)), m1.get((x,3)), m1.get((x,4)))
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
		solo_h_list_a: HashMap::new(),
		solo_h_list_b: HashMap::new(),
		solo_c_list: HashMap::new(),
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

fn print_algo(algo: Algorithm, num_terms: usize, mat_size: (usize, usize)){

	println!("NUMTERMS: {}", num_terms);

	for x in 1..num_terms+1{
	
		let mut term_name = String::from("h");
		term_name.push_str(x.to_string().as_str());
		
		println!("{}: {}", term_name, algo.mult_algo[&term_name]);
	
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

fn mutate(mut algo: Algorithm, term_size: u32, mut num_terms: usize) -> (Algorithm, usize){

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
	let mut mutation_type: usize = rng.gen_range(1..9);
	
	if mutation_type == 1{
		
		let mut h_to_add = String::from("h");
		h_to_add.push_str((num_terms+1).to_string().as_str());
		
		let mut new_h_list = make_h_list(term_size);
		let mut new_h = make_h(&new_h_list);
		
		algo.h_term_lists.insert(h_to_add, new_h_list);
		algo.mult_algo.insert(h_to_add, new_h);
		
		//Also add this new h to one of the c's
		
		let mut row: usize = rng.gen_range(1..6);
		let mut col: usize = rng.gen_range(1..6);
		
		let mut c_to_add_to = String::from("c");
		c_to_add_to.push_str(row.to_string().as_str());
		c_to_add_to.push_str(col.to_string().as_str());
		
		let mut random: usize = rng.gen_range(0..2);
		let mut new_h_name = String::from(" - "); 
		
		if random == 0{ new_h_name.push_str(h_to_add.as_str());}
		
		algo.c_term_lists[&c_to_add_to].push(new_h_name);
		algo.mult_algo.insert(c_to_add_to, make_c(&algo.c_term_lists[&c_to_add_to]));
		
		num_terms += 1;
		
	} else if mutation_type == 2{
	} else if mutation_type == 3{
	} else if mutation_type == 4{
	} else if mutation_type == 5{
	} else if mutation_type == 6{
	} else if mutation_type == 7{
	} else if mutation_type == 8{
	}
	
	(algo, num_terms)

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
	

	
	//algo.mult_algo.insert("Key".to_string(),"Value".to_string());


	//println!("Value of Key: {}", algo.mult_algo["Key"]);
	
	Matmult.start_terms = Matmult.mat_size.0 * Matmult.mat_size.0 * Matmult.mat_size.1; // Init start_terms
	Matmult.num_terms = Matmult.start_terms; 					    // Init num_terms
	Matmult.num_triples = 5;							    // Init num_triples	
	
	let mut algo = rand_algo(Matmult.MEDIUM, Matmult.num_terms, Matmult.mat_size);
	
	println!("Matrix size: {:?}", Matmult.mat_size); // :? operator within {} prints an array's (or vector's apparently) elements
	
	println!("Number of Arguments: {}", &args.len()-1);
	
	println!("Testing multiple prints of tuple: {} {} {:?}", Matmult.mat_size.0, Matmult.mat_size.1, Matmult.mat_size);
	
	//init_mats(&mut Matmult.mat_triples, Matmult.num_triples, Matmult.mat_size);
	//make_h(&make_h_list(Matmult.MEDIUM));
	//make_c(&make_c_list(Matmult.MEDIUM, Matmult.num_terms));
	print_algo(algo, Matmult.num_terms, Matmult.mat_size);
	
	let mut stringy = String::from("1 2 3 4 5");
	//stringy = stringy[0..2].to_string();
	stringy = stringy.replacen(" ", "", 1);
	
	
}
