#include <iostream>
#include <cstring>
#include <vector>
#include <set>

bool gt_int(const int a, const int b) { 
    return a > b;
}

bool gt_char(const char a, char b) {
    return a > b;
}

bool gt_str(const char* a, const char* b) {
    return strcmp(a,b);
}

template <typename Iterator, typename Predicate>
    Iterator mymax(Iterator first, Iterator last, Predicate pred){
        Iterator argmax = first;
        for (Iterator it=first;it!=last;++it) {
            if (pred(*it,*argmax)) argmax = it;
        }
        return argmax;
}

int main() {
    std::cout << "Array" << std::endl;
    int arr_int[] = {1,3,5,7,4,6,9,2,0};
    const int* maxint = mymax( &arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int);
    std::cout << *maxint << std::endl;

    std::cout << "vec" << std::endl;
    std::vector<int> vec_int {1,3,5,7,4,6,9,2,0};
    auto max_iter = mymax(vec_int.begin(), vec_int.end(), gt_int);
    std::cout << *max_iter << std::endl;

    std::cout << "set" << std::endl;
    std::set<int> myset;
    myset.insert(1);myset.insert(3);myset.insert(5);myset.insert(7);myset.insert(4);
    myset.insert(6);myset.insert(9);myset.insert(2);myset.insert(0);
    auto max_set = mymax(myset.begin(),myset.end(),gt_int);
    std::cout << *max_set << std::endl;

    std::cout << "Vector (characters)" << std::endl;
    std::vector<char> vec_char {'a', 'z', 'r', 'm', 'x', 'b'};
    auto max_char_iter = mymax(vec_char.begin(), vec_char.end(), gt_char);
    std::cout << *max_char_iter << std::endl;

    std::cout << "Vector (strings)" << std::endl;
    std::vector<const char*> vec_str {"apple", "banana", "cherry", "date", "elderberry"};
    auto max_str_iter = mymax(vec_str.begin(), vec_str.end(), gt_str);
    std::cout << *max_str_iter << std::endl;

    return 0;
}