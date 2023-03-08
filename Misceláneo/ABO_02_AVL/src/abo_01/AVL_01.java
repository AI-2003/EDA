/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package abo_01;

/**
 *
 * @author rgamboah
 */
public class AVL_01 
{
    public static void reportaArbol(Cls_AVL abo)
    {
        int numNodos = abo.num_nodos();
        int altura   = abo.altura();
        System.out.println("El AboAVL tiene " + numNodos + " nodos");
        System.out.println("Altura del arbol:" + altura);
        double capacidad = (long)Math.pow(2.0,(double)altura) - 1;
        double densidad  = 100.0 * ((double)numNodos) / (double)capacidad;
        String strDensidad=String.format("%5.2f",densidad);
        System.out.println("La capacidad de abo es " + capacidad + " y la densidad es de " + strDensidad + "%");
        
        int numNodos_Nivel[] = new int[altura];
        double  dens_Nivel[] = new double[altura];
        double cotas[] = abo.cotasParaCompactado();
        
        abo.obtenNodosPorNivel(numNodos_Nivel);
        
        for(int nivel = 0; nivel < numNodos_Nivel.length; nivel ++)
        {
               dens_Nivel[nivel] = 100.0 * ((double)(numNodos_Nivel[nivel]) / Math.pow(2.0,nivel));
               System.out.println("Nivel[" + String.format("%3d",(nivel+1)) + "]:" + 
                                             String.format("%3d",numNodos_Nivel[nivel]) + " nodos, densidad: " + 
                                             String.format("%6.2f",dens_Nivel[nivel])+"%, cota para ser compacto: "+
                                             String.format("%6.2f", cotas[nivel])+"%"
               );
        }
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args)
    {
        
        Long SEMILLA = args.length > 0 ? Long.parseLong(args[0]): (long) (10000.0 * Math.random() + 1);
        java.util.Random rnd = new java.util.Random(SEMILLA);
        
        int N = 100;
        int[] arr = new int[N];
        int x;
        
        Cls_AVL abo = new Cls_AVL();
        Cls_AVL aboComp = new Cls_AVL();
        
        for( int i = 0; i < N; i++)
        {
            System.out.println("----------------------------------");
            x = rnd.nextInt();
            arr[i] = x;
            abo.agrega(x);
            System.out.println("Agregando, nodos:" + i);
            reportaArbol(abo);
        }
        System.out.println("ABO:\n" + abo);
        
                System.out.println("--------------------------------------------------");
       if( abo.verificaAlturas())
            System.out.println("OK");
       else
            System.out.println("Problemas con las alturas...");

        AVL_01.reportaArbol(abo);
        
        System.out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++");
        System.out.println("                    Segunda parte");
        System.out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++");

        //System.exit(1);
        
        for(int i = 0; i < N; i++)
            System.out.println("arr["+i+"]:" + arr[i]);
        
        int z = arr[8];
        System.out.println("Buscando " + z + ":\n" + abo.busca(z));
        
        
        //Borra nodos
        
        /*int LIM = N; //N;
        for( int k = 0; k < LIM; k++)
        {
           System.out.println("---------------------------"); 
           System.out.println("Eliminando arr[" + k + "]:" + arr[k]);
           // if(k==5) 
           //     System.out.println("k:"+k);
           abo.elimina(arr[k]);
           //System.out.println("Post:\n" + abo);
           //System.out.println("altura:" + abo.altura() + ", " + abo.num_nodos() + " nodos, densidad:" + abo.densidad() );
           reportaArbol(abo);
           
        }*/
        
        
        System.out.println("SEMILLA:" + SEMILLA);
        
        System.out.println();
        reportaArbol(abo);
        System.out.println("\nViene lo bueno:");
        aboComp = abo.compactado();
        reportaArbol(aboComp);
        
    }
    
}
