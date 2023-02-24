/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package mochila_01;

/**
 *
 * @author rafael
 */
public class Mochila_01 
{
    public static String repBase(int base, int num, int N)
    {
        StringBuilder sb = new StringBuilder();
        for( int k = 0; k < N; k++)
        {
            sb.append(num % base);
            num = (int) ( num / base);
        }
        
        return sb.toString();
    }

    public static void genPesosYValores(java.util.Random rnd, 
                                        int N,
                                        double[] pesos,
                                        double[] valores, 
                                        double PESO_MIN,double PESO_MAX,
                                        double VAL_MIN, double VAL_MAX, 
                                        int start)
    {
        
        
        
        double deltaP = PESO_MAX - PESO_MIN;
        double deltaV = VAL_MAX  - VAL_MIN;
        
        int k;
        for( k = start; k < start+N; k++)
        {
            pesos[k]   = PESO_MIN + deltaP * rnd.nextDouble();
            valores[k] = VAL_MIN  + deltaV * rnd.nextDouble();
        }
    }

    public static int convDec(int N,int base,String strComb)    
    {
        int res = 0;
       
        for(int k = N-1;k >=0;k--)
            res = res * base + (int)(strComb.charAt(k) - '0');
        return res;
    }
    
    private static void desplazaDerechaDesde (Solucion[] sol, int desde){
        
        for(int i=sol.length-1; i>desde; i--){
            sol[i] = sol[i-1];
        }
    }
    
    private static void imprimeInstrucciones(){
        System.out.println("Uso: ");
        System.out.println("Caso 1: java -jar Mochila_01.jar Ej1 SEMILLA");
        System.out.println("Caso 2: java -jar Mochila_01.jar Ej2 RepeticionesPorArtículo SEMILLA");
        System.out.println("El valor de RepeticionesPorArtículo debe ser 0, 1 o 2");
        System.out.println("En ambos casos el argumento SEMILLA es opcional");
    }
    
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) 
    {
        Long SEMILLA;
        
        int    N;
        double CAPACIDAD;
        int base;

        double PESO_MIN;
        double PESO_MAX;
        double VAL_MIN;
        double VAL_MAX;

        java.util.Random rnd;

        double pesos[];
        double valores[];

        int card;

        double valor_comb;
        double peso_comb;
        String strComb;
        
        int cuantos;

        // Variables nuevas
        int numEjecuciones;
        Solucion sol;
        int topSols;
        int i;
        Solucion[] sols;
        int nVeces = 1; // Cuantas veces puede estar presente cada artículo
        int argSemilla = 1; // En qué lugar de los args está la semilla
        boolean validArgs = false;
        double t0, t1;
        
        //Checamos argumentos
        if (args.length > 0){
            if(args[0].equals("Ej1") && args.length<=2)
                validArgs=true;
            if(args[0].equals("Ej2") && args.length<=3){
                argSemilla = 2;
                if(args.length > 1){
                    nVeces = Integer.parseInt(args[1]);
                    if(nVeces>=0 && nVeces<=2)
                        validArgs = true;
                }
            }
        }
        
        // Corremos si todo está en orden
        if(validArgs)
        {
            numEjecuciones  = 10;
            t0 = System.nanoTime();
            for(int ejec=1; ejec<=numEjecuciones; ejec++)
            {
                System.out.println("---------- Ejecucion "+ejec+" ----------\n");

                SEMILLA = args.length > argSemilla ? Long.parseLong(args[argSemilla]): 
                                             (long) (10000.0 * Math.random() + 1);
                
                //Parámetros de generación
                N = 10;
                CAPACIDAD = 20.0;
                base  = 2;
                PESO_MIN = 0.5;
                PESO_MAX = 4.5;
                VAL_MIN  = 1000.0;
                VAL_MAX  = 2500.0;

                pesos   = new double[N*nVeces];
                valores = new double[N*nVeces];

                //Se permite nVeces cada artículo
                for(int rep=0; rep<nVeces; rep++){
                    rnd = new java.util.Random(SEMILLA);
                    genPesosYValores(rnd,N,pesos,valores, PESO_MIN,PESO_MAX,VAL_MIN,VAL_MAX, rep*N);
                }
                N *= nVeces;

                
                card  = (int) Math.pow((double)base,(double)N);

                //Mejores soluciones
                topSols = 10;
                sols = new Solucion[topSols];

                //Evaluamos subconjuntos
                for( int comb = 1; comb < card; comb++)
                {
                   valor_comb = 0.0;
                   peso_comb  = 0.0;
                   strComb    = repBase(base,comb,N);
                   for(int k = 0; k < N; k++)
                   {
                       cuantos = (int)(strComb.charAt(k)-'0');
                       valor_comb += cuantos * valores[k];
                       peso_comb  += cuantos * pesos[k];
                   }


                   if(peso_comb <= CAPACIDAD)
                   {
                       sol = new Solucion(strComb, valor_comb, peso_comb);
                       
                       // Buscamos su lugar entre las mejores soluciones
                       // Recorremos hasta no haya solución en esa posición o hasta que la solución actual tiene un valor mayor
                       i = 0;
                       while(i<sols.length && sols[i]!=null && sol.valorTot<=sols[i].valorTot)
                           i++;
                       
                       // Si la sol no fue menor que todos en el arreglo, desplazamos un lugar abajo las soluciones con menor valor y agregamos la actual
                       if (i != sols.length){
                           // En caso de que estemos evaluando artículos con clones, verificamos que no sea reflexión
                           if(nVeces<2 || i==0 || sols[i-1].esEquivalente(sol)){
                               desplazaDerechaDesde(sols, i);
                               sols[i] = sol;
                           }
                       }
                   }

                }

                //Imprimimos algunos parámetros
                System.out.println("La SEMILLA tiene el valor " + SEMILLA);
                System.out.println("CAPACIDAD:" + CAPACIDAD);
                System.out.println();

                //Imprimimos soluciones
                i=0;
                while (i<topSols && sols[i]!=null){
                    sol = sols[i];
                    i++;
                    System.out.println("Solución en lugar "+i);
                    System.out.println("Combinación:" + sol.strComb);
                    System.out.println("En decimal:" + convDec(N,base,sol.strComb));
                    System.out.println("  Valor Max:" + sol.valorTot);
                    System.out.println("  Peso Comb:"+ sol.pesoTot);
                    System.out.println();
                }
                
                //Indicamos si no hubo tantas soluciones como deseábamos
                if(i!=topSols)
                    if(i==0)
                        System.out.println("\nNo hay soluciones.");
                    else
                        System.out.println("\nNo hay mas soluciones.");
            }
            t1 = System.nanoTime();
            System.out.println("\nTiempo promedio de ejecución por ciclo: "+((t1-t0)/(double) numEjecuciones)+" nseg.");
        }
        else
            // Informamos al usuario sobre el correcto funcionamiento
            imprimeInstrucciones();
    }  
}
