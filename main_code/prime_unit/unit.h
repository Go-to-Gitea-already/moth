#include <iostream>
#include <cmath>
#include <iterator>
#include <vector>

using namespace std;

class PrimeUnit{
     private:
	int distance;

     public:
	int x;
	int y;

        PrimeUnit(){
	    this->x = 0;
	    this->y = 0;
	    this->distance = 0;
	}
        PrimeUnit(int x, int y, int distance){
	    this->x = x;
	    this->y = y;
	    this->distance = distance;
        }

	int check_requests(std::vector<PrimeUnit> units, std::vector<int> kinds_of_bases){
	    constexpr int num_units = { sizeof(units) };
 	    int i = 0;

	    for(int i{ 0 }; i < num_units; i++){
	    // for(PrimeUnit another_unit : units){
		PrimeUnit another_unit = units[i];

		if (&another_unit != this){
		    float dx = another_unit.y - this->x;
		    float dy = another_unit.y - this->y;
		    if (sqrt(dx * dx + dy * dy) < this->distance){
			constexpr int num_kinds_of_bases = { sizeof(kinds_of_bases) };
			int j = 0;
			for(int j{ 0 }; j < num_kinds_of_bases; j++){
			// for(int key : kinds_of_bases){
			    int key = kinds_of_bases[j];
			    // cout << "man, listen from " << this->x << ";" << this->y;
			    another_unit.listen(units, this, key);
			}
		    }
		}
	    }
	    return 0;
	}

	int listen(std::vector<PrimeUnit> units, PrimeUnit* unit, int base_kind){
	    // cout << "man, i am listening at " << this->x << ";" << this->y;
	    return 0;
	}

};

