/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package abo_01;

import java.util.List;

/**
 *
 * @author rgamboah
 */
public class Cls_Nodo_AVL 
{
     public static boolean blnInforma = true;
     
     int dato;
     Cls_Nodo_AVL izq;
     Cls_Nodo_AVL der;
     private int hizq, hder, des;
     
     Cls_Nodo_AVL( int llave)    
     {
         this.dato = llave;
         izq = null;
         der = null;
         hizq = 0;
         hder = 0;
         des = 0;
     }

     protected int getDato()
     {
         return this.dato;
     }

     public int des() { return hder - hizq; }

    public int h()
    {
      return hder > hizq ? hder : hizq;
    }

    boolean verificaAlturas()
    {
      boolean blnRes, blnIzq = true, blnDer = true;
      int hizq_v,hder_v;

      if( izq != null ) blnIzq = izq.verificaAlturas();
      if( der != null ) blnDer = der.verificaAlturas();

      hizq_v = izq != null ? (izq.h() + 1 ): 0;
      hder_v = der != null ? (der.h() + 1 ): 0;

      blnRes = blnIzq && blnDer;
      if ( hizq != hizq_v || hder != hder_v )
      {
          blnRes = false;
          if(Cls_Nodo_AVL.blnInforma) System.out.println("Diferencia en alturas en el nodo " + dato +
                             "hizq:" + hizq + ", hizq_v:" + hizq_v + '\n' +
                             "hder:" + hder + ", hder_v:" + hder_v);
      }
      if( des >= 2 || des <= -2 )
      {
          blnRes = false;
          System.out.println("Desequilibrio en el nodo " + dato +
                             " des: " + des + ", hder: " + hder + ", hizq: " + hizq);
      }

      return blnRes;
    }
 
    // ====================== Rotaciones =======================
     
    public static Cls_Nodo_AVL rotacionDerecha( Cls_Nodo_AVL ap)
    {
      Cls_Nodo_AVL a;
      Cls_Nodo_AVL b,c;
    
      if(Cls_Nodo_AVL.blnInforma) System.out.println("Rotación Derecha sobre el " + ap.getDato());

      a = ap;
      b = ap.izq;
      c = ap.izq.der;

      ap    = b;
      a.izq = c;
      b.der = a;

      ap.der.hizq = ap.der.izq != null ? ap.der.izq.h()+1: 0;
      ap.der.des = ap.der.hder - ap.der.hizq;
      ap.hder = ap.der.h() + 1;
      ap.des = ap.hder - ap.hizq;

      return ap;
    }

    public static Cls_Nodo_AVL rotacionIzquierda( Cls_Nodo_AVL ap)
    {
      Cls_Nodo_AVL a;
      Cls_Nodo_AVL  b,c;
      if(Cls_Nodo_AVL.blnInforma) System.out.println("Rotación Izquierda sobre el " + ap.getDato());

      a = ap;
      b = ap.der;
      c = ap.der.izq;

      ap    = b;
      a.der = c;
      b.izq = a;

      ap.izq.hder = ap.izq.der != null ? ap.izq.der.h()+1: 0;
      ap.izq.des = ap.izq.hder - ap.izq.hizq;
      ap.hizq = ap.izq.h() + 1;
      ap.des = ap.hder - ap.hizq;

      return ap;
    }

    public static Cls_Nodo_AVL rotacionIzquierdaDerecha( Cls_Nodo_AVL ap)
    {
      if(Cls_Nodo_AVL.blnInforma) System.out.println("Rotación izquierdaDerecha sobre el " + ap.getDato());
      ap.izq = Cls_Nodo_AVL.rotacionIzquierda(ap.izq);
      ap = Cls_Nodo_AVL.rotacionDerecha(ap);
      return ap;
    }

    public static Cls_Nodo_AVL rotacionDerechaIzquierda( Cls_Nodo_AVL ap)
    {
      if(Cls_Nodo_AVL.blnInforma) System.out.println("Rotación DerechaIzquierda sobre el " + ap.getDato());
      ap.der = Cls_Nodo_AVL.rotacionDerecha(ap.der);
      ap = Cls_Nodo_AVL.rotacionIzquierda(ap);
      return ap;
    }
 
    public static Cls_Nodo_AVL verificaYEquilibra( Cls_Nodo_AVL ap )
    {
      if( ap.des() == -2 )
      {
        if( ap.izq.des() == -1 )
            ap = Cls_Nodo_AVL.rotacionDerecha(ap);
        else
            if( ap.izq.des() == 1 )
                ap = Cls_Nodo_AVL.rotacionIzquierdaDerecha(ap);
      }
      else
        if( ap.des() == 2 )
        {
          if( ap.der.des() == 1  )
              ap = Cls_Nodo_AVL.rotacionIzquierda(ap);
          else
              if( ap.der.des() == -1 )
                  ap = Cls_Nodo_AVL.rotacionDerechaIzquierda(ap);
        }
        return ap;
    }

    // ============== Fin de Rotaciones ============== 
    
     protected boolean agrega(int llave)
     {
         boolean res = false; // si ya existe regresa false
         if( llave == this.dato )
         {
             return false; // tapón
         }
         if( llave < this.dato)
         {
             if( izq == null)
             {
                 this.izq = new Cls_Nodo_AVL(llave);
                 res = true;
             }
             else
                 res = this.izq.agrega(llave);
             if(res) // lo agregó aquí o en su subarbol izquierdo
             {
                 izq = verificaYEquilibra(izq);
                 hizq = izq.h() + 1;
                 des = hder - hizq;
             }    
         }
         else
         {
             if( der == null)
             {
                 this.der = new Cls_Nodo_AVL(llave);
                 res = true;
             }
             else
                 res = der.agrega(llave);
             if(res)
             {
                 der = verificaYEquilibra(der);
                 hder = der.h() + 1;
                 des = hder - hizq;
             }
         }
         return res;
     }
     
     protected boolean agregaSinVerificar(int llave)
     {
         boolean res = false; // si ya existe regresa false
         if( llave == this.dato )
         {
             return false; // tapón
         }
         if( llave < this.dato)
         {
             if( izq == null)
             {
                 this.izq = new Cls_Nodo_AVL(llave);
                 res = true;
             }
             else
                 res = this.izq.agregaSinVerificar(llave);
             if(res) // lo agregó aquí o en su subarbol izquierdo
             {
                 hizq = izq.h() + 1;
                 des = hder - hizq;
             }    
         }
         else
         {
             if( der == null)
             {
                 this.der = new Cls_Nodo_AVL(llave);
                 res = true;
             }
             else
                 res = der.agregaSinVerificar(llave);
             if(res)
             {
                 hder = der.h() + 1;
                 des = hder - hizq;
             }
         }
         return res;
     }
     
     protected String busca( int llave)
     {
         if( this.getDato() == llave)
             return ":" + llave;
         
         if( llave < this.getDato() )    
         {
             if(this.izq == null)
                 return "No existe";
             else
                 return "Izq " + this.izq.busca(llave);
         }
         else
         {
             if(this.der == null)
                 return "No existe";
             else
                 return "Der " + this.der.busca(llave);
         } 
     }
     
    protected void elimina(int llave)
    {
         Cls_Nodo_AVL hijo_mayor;
         Cls_Nodo_AVL hijo_menor;
         // este nodo recibe la orden pero no tiene la llave como dato
         if( llave < this.dato )
         {
             if( this.izq != null )
             {
                 if( this.izq.dato == llave )
                 {
                     // elimina el nodo en this.izq ...
                     System.out.println("Se localizó el nodo con el dato " + this.izq.dato + " para la llave " + llave);
                     // -------------------------------
                      if(this.izq.izq != null)
                      {
                          // trae el hijo_mayor del subarbol izq
                          hijo_mayor = this.izq.hijoMayor();
                          hijo_mayor.der = this.izq.der;
                          hijo_mayor.izq = this.izq.izq;
                          this.izq = hijo_mayor;
                      }
                      else
                      {
                          if( this.izq.der != null)
                          {
                              // trae el hijo_menor del subarbol derecho
                              hijo_menor = this.izq.hijoMenor();
                              hijo_menor.der = this.izq.der;
                              hijo_menor.izq = this.izq.izq;
                              this.izq = hijo_menor;
                          }
                          else
                          {
                              // ambos subarboles son nulos
                              this.izq = null;
                          }
                      }
                   // -------------------------------
                 }
                 else
                 {
                   this.izq.elimina(llave);
                 }   
             }
             
         }
         else // caso para la llave > dato
         {
             if(this.der != null )
             {
                 if( this.der.dato == llave )
                 {
                     // elimina el nodo en this.der ...
                      System.out.println("Se localizó el nodo con el dato " + this.der.dato + " para la llave " + llave);
                      if(this.der.izq != null)
                      {
                          // trae el hijo_mayor del subarbol izq
                          hijo_mayor = this.der.hijoMayor();
                          hijo_mayor.der = this.der.der;
                          hijo_mayor.izq = this.der.izq;
                          this.der = hijo_mayor;
                      }
                      else
                      {
                          if( this.der.der != null)
                          {
                              // trae el hijo_menor del subarbol derecho
                              hijo_menor = this.der.hijoMenor();
                              hijo_menor.der = this.der.der;
                              hijo_menor.izq = this.der.izq;
                              this.der = hijo_menor;
                          }
                          else
                          {
                              // ambos subarboles son nulos
                              this.der = null;
                          }
                      }
                 }
                 else
                 {
                     this.der.elimina(llave);
                 }
             }
         }
             
    }

    protected Cls_Nodo_AVL hijoMayor()
    {
        // estamos en un nodo, quebramos a la izq y luego puras derechas
        // y el nodo tiene hijo izq.
        Cls_Nodo_AVL nodo_padre = this;
        Cls_Nodo_AVL hijo_mayor;
        if( izq.der == null )
        {
          // recupero el apuntador a nodo y lo libero
          hijo_mayor = this.izq;
          this.izq   = hijo_mayor.izq; 
        }
        else // el nodo izq.der existe 
        {
          nodo_padre = this.izq;
          while( nodo_padre.der.der != null ) nodo_padre = nodo_padre.der;
          // recupero el apuntador y lo libero
          hijo_mayor = nodo_padre.der;
          nodo_padre.der = hijo_mayor.izq;
        }
        return hijo_mayor;
    }

    protected Cls_Nodo_AVL hijoMenor()
    {
        // estamos en el nodo a borrar, quebramos a la izq y luego puras derechas
        // y el nodo tiene hijo izq.
        Cls_Nodo_AVL nodo_padre = this;
        Cls_Nodo_AVL hijo_menor;
        if( der.izq == null )
        {
          // recupero el apuntador a nodo y lo libero
          hijo_menor = this.der;
          this.der   = hijo_menor.der; 
        }
        else // el nodo izq.der existe 
        {
          nodo_padre = this.der;
          while( nodo_padre.izq.izq != null ) nodo_padre = nodo_padre.izq;
          // recupero el apuntador y lo libero
          hijo_menor = nodo_padre.izq;
          nodo_padre.izq = hijo_menor.der;
        }
        return hijo_menor;
    }
    
    public int altura()
    {
        int h_izq,h_der;
        h_izq = izq == null ? 0 : izq.altura();
        h_der = der == null ? 0 : der.altura();
        return  1 + ( h_izq > h_der ? h_izq : h_der );
    }
    
    public void num_nodos(int c[])
    {
        c[0]++;
        if( izq != null ) izq.num_nodos(c);
        if( der != null ) der.num_nodos(c);
    }

    public void obtenNodos_Nivel(int nivel,int numNodos_nivel[])
    {
      numNodos_nivel[nivel]++;
      if(izq != null ) izq.obtenNodos_Nivel( nivel + 1, numNodos_nivel);
      if(der != null ) der.obtenNodos_Nivel( nivel + 1, numNodos_nivel);
    }
    
    public void obtenllaves(int llaves[], int van[])
    {
      if( this.izq != null) this.izq.obtenllaves(llaves, van);
      van[0]++;
      llaves[van[0]] = this.dato;
      if( this.der != null) this.der.obtenllaves(llaves, van);
    }
    
    public void ordena (List<Integer> datos){
        if(this.izq!=null) izq.ordena(datos);
        datos.add(this.dato);
        if(this.der!=null) der.ordena(datos);
    }

     @Override
     public String toString()
     {
         StringBuilder sb = new StringBuilder();
         if( this.izq != null) sb.append(this.izq);
         sb.append(this.getClass().getName()).append(':').append(this.dato).append('\n');
         if( this.der != null ) sb.append(this.der);
         return sb.toString();
     }
}
