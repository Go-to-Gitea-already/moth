#include <iostream>
#include <cmath>
#include <iterator>
#include <vector>
#include <map>

using namespace std;

class PrimeUnit{
     private:
	int k;

     public:
	int x;
	int y;
    	float rotation;
	int distance;
	int destiny;
	std::map<int, int> points;

        PrimeUnit(){
	    this->x = 0;
	    this->y = 0;
	    this->distance = 0;
	    this->rotation = 0;
	    this->points = {};
	}

        PrimeUnit(int x, int y, int distance, float rotation, std::vector<int> kinds_of_bases){
	    this->x = x;
	    this->y = y;
	    this->distance = distance;
	    this->rotation = rotation;
	    this->points = {};
	    for (int key : kinds_of_bases){
		this->points[key] = this->distance + 1;
	    }
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
	
	int check_responses(std::vector<PrimeUnit> units, int base_kind){
	    constexpr int num_units = { sizeof(units) };
 	    int i = 0;

	    for(int i{ 0 }; i < num_units; i++){
	    // for(PrimeUnit another_unit : units){
		PrimeUnit another_unit = units[i];

		if (&another_unit != this){
		    float dx = another_unit.y - this->x;
		    float dy = another_unit.y - this->y;
		    if (sqrt(dx * dx + dy * dy) < this->distance){
		        another_unit.listen(units, this, base_kind);
		    }
		}
	    }
	    return 0;
	}

	int listen(std::vector<PrimeUnit> units, PrimeUnit* unit, int base_kind){
	    if(this->points[base_kind] > unit->points[base_kind] + this->distance * 1){
		    this->points[base_kind] = unit->points[base_kind] + this->distance;

		    if(base_kind == this->destiny){
			float dx = unit->x - this->x;
			float dy = unit->y - this->y;

			// dx = this->x - unit->x;
			// dy = this->y - unit->y;

			if(dx == 0){
			    dx = 0.00000001;
			}

			// this->rotation = atan(dy / dx) + M_PI % (2 * M_PI);
			this->rotation = atan(dy / dx);

			if(0 > dx){
			    this->rotation = std::fmod((this->rotation + M_PI), (2 * M_PI));
			}

			if(this->rotation < 0){
			    this->rotation = 2 * M_PI + this->rotation;
			}
		    }

		    this->check_responses(units, base_kind);
	    }

	    return 0;
	}

};

