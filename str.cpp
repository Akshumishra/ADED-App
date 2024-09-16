#include<iostream>
#include<string>
#include<vector>
using namespace std;
int main(){
    string str;
    cin>>str;
    int maxi=0;
    int count=1;
    int n=str.length();
    for(int i=1;i<n;i++){
        if(str[i]==str[i-1]){
            count++;
            maxi=max(count,maxi);
        }
        else{
            count=1;
        }
    }
    cout<<maxi;
}