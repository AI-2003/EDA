/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package mochila_01;

/**
 *
 * @author carlo
 */
public class Solucion {
    String strComb;
    double valorTot;
    double pesoTot;
    
    public Solucion (String strComb, double valorTot, double pesoTot) {
        this.strComb = strComb;
        this.valorTot = valorTot;
        this.pesoTot = pesoTot;
    }
    
    //Checa si el binario es una reflexión sobre el eje verical 
   public boolean esEquivalente(Solucion sol){
        boolean res=true;
        int i, n;
         
        n = strComb.length();
        i=0;
        while(i<(n/2) && strComb.charAt(i)==sol.strComb.charAt(n-1-i))
            i++;
        if(i<(n/2))
            res=false;
        return res;
    }
}
