# -*- coding: utf-8 -*-

# =============================================================================
#                                Utilerías Generales
# =============================================================================
import sys
import time
import datetime

cadsep = "=" * 60

def letrero(strLetrero):
    print(cadsep)
    print("          " + strLetrero)
    print(cadsep)

def salir(strLetrero):
    letrero(strLetrero)
    sys.exit()	
# =============================================================================
#   Asigne su CU y nombre como cadenas de caracteres
# =============================================================================
CU     = '201598'
NOMBRE = 'IBARRARAN ARNALDO CARLOS ARMANDO'

def print_id():
    global CU
    global NOMBRE
    print(cadsep)
    print('CU:' + CU + ' ... ' + NOMBRE)
    print(cadsep)

def progMateriaNombre():
   str_dateTime   = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
   print(cadsep)
   print('         COM-11103 Estructuras de Datos Avanzadas')
   print('              semestre enero - mayo 2023, Gpo 02')
   print('                 Segundo Examen Parcial')
   print(' '*18 + str_dateTime)
   print_id()

# =============================================================================
#                                Clases de la Contabilidad
# =============================================================================
	
# -----------------------------------------------------------------------------
#                                Contabilidad
# -----------------------------------------------------------------------------

class Contabilidad:
    def __init__(self,ejer,nombre):
        self.ejercicio = ejer
        self.nombre    = nombre
        self.colPartes = [0] * 6
        self.colPartes[1] = ParteContable(1,"Activo  ","D")
        self.colPartes[2] = ParteContable(2,"Pasivo  ","A")
        self.colPartes[3] = ParteContable(3,"Capital ","A")
        self.colPartes[4] = ParteContable(4,"Ingresos","A")
        self.colPartes[5] = ParteContable(5,"Egresos ","D")
        self.colPolizas = {} 
#
# -----------------------------------------------------------------------------
#      
    def altaCta(self,id_cta,nomCta,natCta):
        #print("Se va a dar de alta la cuentaT:" +
        #      str(id_cta) + " " + nomCta + " (" + natCta + ")")
        #
        # identificamos la parte a la que le corresponde la responsabilidad de 
        # dar de alta la cta
        #
        idParte = id_cta // 100000
        if idParte < 1 or 5 < idParte :
            raise Exception("la parte " + str(idParte) + " en la cta " + str(id_cta) + " no existe")
        else:
            if self.colPartes[idParte].existeCta(id_cta):
              raise Exception("la cta " + str(id_cta) + " ya existe")  
            else:
              self.colPartes[idParte].altaCta(id_cta,nomCta,natCta)  
#
# -----------------------------------------------------------------------------
#      
    def registraPoliza(self,pol):
        blnRes = True
        #
        #   verificamos que no exista esa póliza
        #
        if self.colPolizas.get(pol.idPoliza) != None:
            raise Exception("La póliza " + str(pol.idPoliza) + " ya existe")


        #
        #   verificamos que la póliza esté cuadrada
        #
        sc = 0
        sa = 0
        for m in pol.colMovtos:
            if m.tipo == "C":
                sc += m.monto
            else:
                sa += m.monto
        if sc != sa:
            print("Poliza descuadrada" + str(pol))
            return False
        
        #
        #   verificamos que existe cada una de las cuentas involucradas
        #
        blnExisteCtas = True
        for m in pol.colMovtos:
            cta = m.numCta
            idParte = cta // 100000
            if idParte < 1 or 5 < idParte:
                blnExisteCtas = False
                print("La cta " + str(cta) + " NO EXISTE")
            else:
                blnExisteCtas = blnExisteCtas and \
                                self.colPartes[idParte].existeCta(cta)
        if not blnExisteCtas:    
            print("Alguna de las cuentas no existe") 
            return False
        #
        #  Todo bien, regisreamos la póliza y los movimientos de la póliza
        #

        # Agregamos la póliza
        self.colPolizas[pol.idPoliza] = pol

        # Agregamis sus movtos
        for m in pol.colMovtos:
            cta = m.numCta
            idParte = cta // 100000
            self.colPartes[idParte].registraMovto(m)
        
        return blnRes
    
#
# -----------------------------------------------------------------------------
#      
    def ecuacion(self):
        saldo_activo   = self.colPartes[1].saldo()
        saldo_pasivo   = self.colPartes[2].saldo()
        saldo_capital  = self.colPartes[3].saldo()
        saldo_ingresos = self.colPartes[4].saldo()
        saldo_egresos  = self.colPartes[5].saldo()
        
        saldo_egresos.tipo = "A"
        saldo_egresos.monto *= -1
        
        strRes = "*" * 43  + '\n'
        
        strRes += str(saldo_activo  ) + '\n'
        strRes += str(saldo_pasivo  ) + '\n'
        strRes += str(saldo_capital ) + '\n'
        strRes += str(saldo_ingresos) + '\n'
        strRes += str(saldo_egresos ) + '\n'
        strRes += "-" * 43 + '\n' 
        strRes += " " * 18 
        strRes += "{:12,.2f}".format(saldo_activo.monto)  + \
                  "{:12,.2f}".format(saldo_pasivo.monto   +
                                     saldo_capital.monto  +
                                     saldo_ingresos.monto +
                                     saldo_egresos.monto) + '\n'
        strRes += "*" * 43 + '\n'
        return strRes
    
#
# -----------------------------------------------------------------------------
#      
    def edoRes(self):
        strRes = "Estado de Resultado:"  + '\n'
        strRes += str(self.colPartes[4]) + '\n'
        strRes += str(self.colPartes[5]) + '\n'
        
        saldo_ingresos = self.colPartes[4].saldo()
        saldo_egresos  = self.colPartes[5].saldo()
        
        saldo_egresos.tipo = "A"
        saldo_egresos.monto *= -1
    
        strRes = "*" * 43  + '\n'
        
        strRes += str(saldo_ingresos) + '\n'
        strRes += str(saldo_egresos ) + '\n'
        strRes += "-" * 43 + '\n' 
        
        strRes += " " * 30 
        strRes +=  "{:12,.2f}".format(saldo_ingresos.monto +
                                      saldo_egresos.monto) + '\n'
        strRes += "*" * 43 + '\n'
        return strRes   
#
# -----------------------------------------------------------------------------
#      
    def cierre(self):
        id_cta_cierre = 300100
        if not self.colPartes[3].existeCta(id_cta_cierre):
             self.altaCta(id_cta_cierre, "Resultado del Ejercicio", "A")
             
        pol_cierre = PolizaContable(self.ejercicio*10000,"Póliza de Cierre",20231231)     
        
        self.colPartes[4].saldaCtas(pol_cierre,id_cta_cierre)
        self.colPartes[5].saldaCtas(pol_cierre,id_cta_cierre)    
    
        blnRes = self.registraPoliza(pol_cierre)

        #Reconocimiento de adeudo
        if blnRes:
            utilidad = self.colPartes[3].ColCtas[id_cta_cierre].saldo().monto
            if utilidad > 0:

                # Verificamos existencia de cuenta de ISR por pagar
                id_cta_adeudo = 200200
                if not self.colPartes[2].existeCta(id_cta_adeudo):
                    self.altaCta(id_cta_adeudo, "ISR por Pagar", "A")
                
                # Disminución de utilidad y aumento de ISR por pagar
                pol_adeudo = PolizaContable(self.ejercicio*10000+1, "Póliza de Adeudo", 20231231)
                pol_adeudo.abono(id_cta_adeudo, utilidad*0.3)
                pol_adeudo.cargo(id_cta_cierre, utilidad*0.3)
                blnRes = blnRes and self.registraPoliza(pol_adeudo)

        return blnRes

#
# -----------------------------------------------------------------------------
#  

    def imprimePolizas(self):
        
        strRes = "\n                        Pólizas\n"
        strRes += "="*60 + "\n" 
        for pol in self.colPolizas.values():
            strRes += str(pol) + "\n" + "=" * 30 + "\n"
        print(strRes)
        

#
# -----------------------------------------------------------------------------
#      
    def __str__(self):
        strRes = str(self.nombre) + " " + str(self.ejercicio) + "\n"
        
        for k in range(1,6):
          strRes += str(self.colPartes[k])
        return strRes
        
# -----------------------------------------------------------------------------
#                               ParteContable
# -----------------------------------------------------------------------------
              
class ParteContable:
    def __init__(self,idParte,nombre,nat):
        self.id        = idParte
        self.nombre    = nombre
        self.nat       = nat
        self.ColCtas   = {}

#
# -----------------------------------------------------------------------------
#      
    def existeCta(self,idCta):
        return self.ColCtas.get(idCta) != None
        
    
#
# -----------------------------------------------------------------------------
#      
    def altaCta(self,id_cta,nomCta,natCta):
        #print("Parte conta:"+str(self.id) +
        #      " Se va a dar de alta la cuentaT:" +
        #      str(id_cta) + " " + nomCta + " (" + natCta + ")")
        self.ColCtas[id_cta] = CuentaContable(id_cta,nomCta,natCta)

#
# -----------------------------------------------------------------------------
#      
    def registraMovto(self,movto):
        cta = movto.numCta
        self.ColCtas[cta].registraMovto(movto)

#
# -----------------------------------------------------------------------------
#      
    def saldo(self):
        sc = 0
        sa = 0
        for k_v in self.ColCtas.items():
          cta = k_v[1]
          if cta.nat == "D":
              sc += cta.saldo().monto
          else:
              sa += cta.saldo().monto
        #strLetrero = "Sdo. " + str(self.id)
        strLetrero = str(self.nombre)[:6]
        if self.nat == "D":
            movto_saldo = MovtoContable("C",strLetrero,sc-sa)
        else:
            movto_saldo = MovtoContable("A",strLetrero,sa-sc)
        return movto_saldo  
        
#
# -----------------------------------------------------------------------------
#      
    def saldaCtas(self,pol_cierre, id_cta_cierre):
        for cta in self.ColCtas.values():
                saldo_cta = cta.saldo()
                if saldo_cta.tipo == "C":
                   pol_cierre.cargo(id_cta_cierre,saldo_cta.monto)
                   pol_cierre.abono(cta.numCta,   saldo_cta.monto)
                else:
                   pol_cierre.abono(id_cta_cierre,saldo_cta.monto)
                   pol_cierre.cargo(cta.numCta,   saldo_cta.monto)
                         
    
#
# -----------------------------------------------------------------------------
#      
    def __str__(self):
        strRes = str(self.id) + " ... " + \
                 self.nombre + " (" + self.nat + ")\n"
        for cta in self.ColCtas.values():
                     strRes += str(cta)
        strRes += "=" * 30 + '\n'
        strRes += str(self.saldo()) + '\n'
        strRes += "=" * 30 + '\n'         
        return strRes

# -----------------------------------------------------------------------------
#                              CuentaContable
# -----------------------------------------------------------------------------

class CuentaContable:
    def __init__(self,idCta,nombre,nat):
        self.numCta    = idCta
        self.nombre    = nombre
        self.nat       = nat
        self.ColMovtos = []
    
#
# -----------------------------------------------------------------------------
#      
    def registraMovto(self,movto):
        self.ColMovtos.append(movto)
        
#
# -----------------------------------------------------------------------------
#      
    def saldo(self):
        sc = 0
        sa = 0
        for m in self.ColMovtos:
            if m.tipo == "C":
                sc += m.monto
            else:
                sa += m.monto        
        if self.nat == "D":
            movto_saldo = MovtoContable("C",self.numCta,sc-sa)
        else:
            movto_saldo = MovtoContable("A",self.numCta,sa-sc)
        return movto_saldo    
        
#
# -----------------------------------------------------------------------------
#      
    def __str__(self):
        strRes = str(self.numCta) + " ... " + \
                 self.nombre + " (" + self.nat + ")\n"
        for m in self.ColMovtos:
            strRes += str(m) + '\n'
        strRes += "-" * 25 + '\n'
        strRes += str(self.saldo()) + '\n'
        strRes += "-" * 25 + '\n'
        return strRes    
# -----------------------------------------------------------------------------
#                                PolizaContable
# -----------------------------------------------------------------------------

class PolizaContable:
    def __init__(self,id,desc,intFecha):
        self.idPoliza    = id
        self.descripcion = desc
        self.fecha       = intFecha
        self.colMovtos   = []
        
#
# -----------------------------------------------------------------------------
#      
    def cargo(self,idCta,monto):
        m = MovtoContable("C", idCta, monto)
        self.colMovtos.append(m)
        
#
# -----------------------------------------------------------------------------
#      
    def abono(self,idCta,monto):
        m = MovtoContable("A", idCta, monto)
        self.colMovtos.append(m)
        
#
# -----------------------------------------------------------------------------
#      
    def __str__(self):
        strRes = "Poliza " + str(self.idPoliza) + " " + \
                 self.descripcion + " " + str(self.fecha) + "\n"
        for m in self.colMovtos:
            strRes += str(m) + "\n"
        return strRes

# -----------------------------------------------------------------------------
#                                MovtoContable
# -----------------------------------------------------------------------------

class MovtoContable:
    def __init__(self,tipo,numCta,monto):
        self.tipo   = tipo
        self.numCta = numCta
        self.monto  = monto

#
# -----------------------------------------------------------------------------
#      
    def __str__(self):
         strRes = "(" + self.tipo + ") " + str(self.numCta)
         if self.tipo == "A":
             strRes += " " * 12
         strRes += "     " + "{:15,.2f}".format(self.monto)
         return strRes
 
# =============================================================================
#                                Script principal
# =============================================================================
progMateriaNombre()
#
# -----------------------------------------------------------------------------
#
conta = Contabilidad(2023, "MiEmpre S.A.")

conta.altaCta(100100,"Bancos               ","D")
conta.altaCta(100200,"Inventario           ","D")
conta.altaCta(200100,"Proveedores          ","A")
conta.altaCta(300000,"Capital              ","A")
conta.altaCta(400100,"Ventas               ","A")
conta.altaCta(500100,"Costo de lo Vendido  ","D")

print(cadsep)
#print(conta)

pol1 = PolizaContable(1,"Constitución de la Empresa",20190121)
pol1.cargo(100100,10000)
pol1.abono(300000,10000)
conta.registraPoliza(pol1)

pol2 = PolizaContable(2,"Compra de mercancía por 3000 pagados al contado",20190122)
pol2.cargo(100200,3000)
pol2.abono(100100,3000)
conta.registraPoliza(pol2)

pol3 = PolizaContable(3,"Venta al contado por 1500 de mercancía que costó 1000",20190122)
pol3.abono(100200,1000)
pol3.cargo(500100,1000)
pol3.abono(400100,1500)
pol3.cargo(100100,1500)
conta.registraPoliza(pol3)

pol4 = PolizaContable(4,"Venta al contado por 1000 de mercancía que costó 750",20190201)
pol4.abono(100200, 750)
pol4.cargo(500100, 750)
pol4.abono(400100,1000)
pol4.cargo(100100,1000)
conta.registraPoliza(pol4)

print(conta)
print(conta.ecuacion())

# =============================================================================
# [3.0]   Ejercicio 1) Agregar el reconocimiento del adeudo del ISR
'''
     En el proceso del cierre contable,
     en caso de haber utilidad (Saldo de la cuenta 300100 es un abono o esta
                                cuenta tiene saldo positivo ),
     generar una póliza con el 30% de la utilidad como adeudo a la cuenta 
                 200200 ISR por Pagar (A)
     y un cargo a la cuenta
                 300100 para disminuir la cantidad de la utilidad posterior
    al ISR.
                 
'''    
# =============================================================================
# [4.0]     Ejercicio 2) Agregar a la contabilidad la colacción de pólizas,
'''
                    El id de la póliza es el número de póliza.
                    La póliza de cierre tiene como id Ejercicio * 10,000
                    La contabilidad debe verificar que no haya pólizas repetidas.
'''
# =============================================================================
# =============================================================================
#  [3.0]    Ejercicio 3) Proceso de generación de pólizas de ventas
'''
             [2.0] Elabore un proceso que genere pólizas de ventas con valores
                   del costo de lo vendido entre c_min y c_max y valor de la venta 
                   un 25%  y 35% del costo de lo vendido.
                   La rutina para generar valores aleatorios se proporciona a
                   continuación
                   
                   El uso que debe tener es
                   
                   pol_vta = genPolVta(id_pol,c_min,c_max)
                   
                   ej:
                       
                  pol_vta = genPoliza(25, 250.0, 400.0)
                  
             [1.0] Agregue el código para el uso por medio de un for adecuado
                  y posteriormente haga el cierre.
                  
                  ¿Qué ocurre con el inventario?

'''


# =============================================================================
import random
def iniciaAleat(SEMILLA):
    random.seed(SEMILLA)
    
def proxValor(valMin,valMax):
    
    return float("{:.2f}".format(0.05*float(int(100*random.uniform(valMin,valMax)+4)//5)))

# =============================================================================


# Generación y registro de pólizas
# =============================================================================

def genPolVta(id_pol, c_min, c_max):
        # Se genera el costo, el valor de venta y la fecha de venta
        costo = proxValor(c_min, c_max)
        valorVenta = costo * proxValor(0.25, 0.35)
        fechaVenta = int(proxValor(20190201, 20190228))

        # Se hace los mvtos
        polVenta = PolizaContable(id_pol, "Venta aleatoria " + str(i), fechaVenta)
        polVenta.abono(100200, costo)
        polVenta.cargo(500100, costo)
        polVenta.abono(400100, valorVenta)
        polVenta.cargo(100100, valorVenta)
        return polVenta


numPolizas = 3
for i in range(numPolizas):
    c_min = int(proxValor(100,1000))
    pol_i = genPolVta(100+i, c_min, c_min + proxValor(100, 300))
    conta.registraPoliza(pol_i)




# =============================================================================

print(cadsep + '\n')
print("              Balance")
print(conta.ecuacion())
print(cadsep + '\n')
print("           Estado de Resultados")
print(conta.edoRes())
print(cadsep + '\n')

conta.cierre()
print("              Balance post cierre")
print(cadsep)
print(conta)
print(cadsep)
print(cadsep)

conta.imprimePolizas()

progMateriaNombre()

#
# ========================== FIN DEL SCRIPT PRINCIPAL =====================


