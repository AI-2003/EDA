/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package abo_01;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author rgamboah
 */
public class Cls_AVL 
{
    Cls_Nodo_AVL raiz = null;
    
    public boolean agrega(int llave)
    {
        boolean res = true;
        if( raiz == null)
        {
            raiz = new Cls_Nodo_AVL(llave);
            res = true;
        }
        else
        {
            res = raiz.agrega(llave);
            if(res) raiz = Cls_Nodo_AVL.verificaYEquilibra(raiz);
        }
        return res;
    }
    
    private boolean agregaSinVerificar(int llave)
    {
        boolean res = true;
        if( raiz == null)
        {
            raiz = new Cls_Nodo_AVL(llave);
            res = true;
        }
        else
        {
            res = raiz.agregaSinVerificar(llave);
        }
        return res;
    }
    
    public int h(){ return raiz.h();}

    public boolean verificaAlturas()
    {
      boolean blnRes = true;
      System.out.println("Verificando alturas...");
      if( raiz != null ) blnRes = raiz.verificaAlturas();
      return blnRes;
    }
    
    public boolean vacio()
    {
        return raiz == null;
    }
    
    public String busca(int llave)
    {
        if( this.vacio())
            return "ABO vacío";
        if( this.raiz.getDato() == llave)
            return "raiz";
        return raiz.busca(llave);
        
    }
    
    public void elimina(int llave)
    {
        Cls_Nodo_AVL hijo_mayor;
        Cls_Nodo_AVL hijo_menor;
        if( raiz == null ) // nada que eliminar
            return;
        if(raiz.getDato() == llave)
        {
            // eliminar la raíz promoviendo al uno de sus descendientes
             System.out.println("Se localizó el nodo raíz con el dato " + raiz.dato + " para la llave " + llave);
             if( raiz.izq != null)
             {
                hijo_mayor = raiz.hijoMayor();
                hijo_mayor.izq = raiz.izq;
                hijo_mayor.der = raiz.der;
                raiz = hijo_mayor;
             }
             else
             {
                 if( raiz.der != null)
                 {
                     hijo_menor = raiz.hijoMenor();
                     hijo_menor.izq = raiz.izq;
                     hijo_menor.der = raiz.der;
                     raiz = hijo_menor;
                 }
                 else
                     raiz = null;
             }
        }
        else
            raiz.elimina(llave);
    }
     
    public int num_nodos()
    {
        int c[] = new int[1];
        c[0] = 0;
        if( raiz != null) raiz.num_nodos(c);
        return c[0];
    }
    
    public int altura()
    {
        return raiz == null ? 0 : raiz.altura();
    }
    
    public double densidad()
    {
        int cant_nodos      = this.num_nodos();
        int h               = this.altura();
        if( h == 0)
            return 0;
        double dblCapacidad = Math.pow(2.0, h) - 1.0;
        return ((double) cant_nodos ) / dblCapacidad;  
    }
    
    
    // Arreglar con colas
    
    // Notas previas a arreglar:
    // Está muy chafa que dependa de los nodos
    // Se propaga la responsabilidad
    // Quitar dependencias funcionalesn , 
    public int[] obtenNodosPorNivel(int[] numNodos_nivel)
    {
      int nivel = 0;
      
        if(raiz != null)
           raiz.obtenNodos_Nivel(nivel,numNodos_nivel);  
        return numNodos_nivel;
    }
    
    private void agregaMitad (Cls_AVL avl, List<Integer> datos, int ini, int fin){
        int mid;
        
        if(fin>=ini){
            mid = (fin+ini)/2;
            avl.agregaSinVerificar(datos.get(mid));
            agregaMitad(avl, datos, ini, mid-1);
            agregaMitad(avl, datos, mid+1, fin);
        }
    }
    
    public Cls_AVL compactado(){
        Cls_AVL avl;
        List<Integer> datos;
        
        //Recorre
        datos = new ArrayList<Integer>();
        if(raiz!=null) raiz.ordena(datos);
        
        //Agrega en orden
        avl = new Cls_AVL();
        agregaMitad(avl, datos, 0, datos.size()-1);
        
        return avl;
    }
    
    @Override
    public String toString()
    {
        String strRes;
        if( raiz == null )
            strRes = "ABO vacío";
        else
           strRes = raiz.toString();
        
        return strRes;
    }
    
}
