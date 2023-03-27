# -*- coding: utf-8 -*-

# =============================================================================
#                                Utilerías Generales
# =============================================================================
import sys

cadsep = "=" * 60

def letrero(strLetrero):
    print(cadsep)
    print("          " + strLetrero)
    print(cadsep)

def salir(strLetrero):
    letrero(strLetrero)
    sys.exit()	
# =============================================================================
#                                Clase de la Contabilidad
# =============================================================================
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
              raise Exception("la cta " + str(idCta) + " ya existe")  
            else:
              self.colPartes[idParte].altaCta(id_cta,nomCta,natCta)  

    def registraPoliza(self,pol):
        blnRes = True
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
            return false
        
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
        #  Todo bien, regisreamos los movimientos de la póliza
        #
        for m in pol.colMovtos:
            cta = m.numCta
            idParte = cta // 100000
            self.colPartes[idParte].registraMovto(m)
        
        return blnRes
    
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
    
    
    def __str__(self):
        strRes = str(self.nombre) + " " + str(self.ejercicio) + "\n"
        
        for k in range(1,6):
          strRes += str(self.colPartes[k])
        return strRes
        
              
class ParteContable:
    def __init__(self,idParte,nombre,nat):
        self.id        = idParte
        self.nombre    = nombre
        self.nat       = nat
        self.ColCtas   = {}

    def existeCta(self,idCta):
        return self.ColCtas.get(idCta) != None
        
    
    def altaCta(self,id_cta,nomCta,natCta):
        #print("Parte conta:"+str(self.id) +
        #      " Se va a dar de alta la cuentaT:" +
        #      str(id_cta) + " " + nomCta + " (" + natCta + ")")
        self.ColCtas[id_cta] = CuentaContable(id_cta,nomCta,natCta)

    def registraMovto(self,movto):
        cta = movto.numCta
        self.ColCtas[cta].registraMovto(movto)

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
        
        
    def __str__(self):
        strRes = str(self.id) + " ... " + \
                 self.nombre + " (" + self.nat + ")\n"
        for cta in self.ColCtas.values():
                     strRes += str(cta)
        strRes += "=" * 30 + '\n'
        strRes += str(self.saldo()) + '\n'
        strRes += "=" * 30 + '\n'         
        return strRes
        
class CuentaContable:
    def __init__(self,idCta,nombre,nat):
        self.numCta    = idCta
        self.nombre    = nombre
        self.nat       = nat
        self.ColMovtos = []
    
    def registraMovto(self,movto):
        self.ColMovtos.append(movto)
        
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
        
    def __str__(self):
        strRes = str(self.numCta) + " ... " + \
                 self.nombre + " (" + self.nat + ")\n"
        for m in self.ColMovtos:
            strRes += str(m) + '\n'
        strRes += "-" * 25 + '\n'
        strRes += str(self.saldo()) + '\n'
        strRes += "-" * 25 + '\n'
        return strRes    

class PolizaContable:
    def __init__(self,id,desc,intFecha):
        self.idPoliza    = id
        self.descripcion = desc
        self.fecha       = intFecha
        self.colMovtos   = []
        
    def cargo(self,idCta,monto):
        m = MovtoContable("C", idCta, monto)
        self.colMovtos.append(m)
        
    def abono(self,idCta,monto):
        m = MovtoContable("A", idCta, monto)
        self.colMovtos.append(m)
        
    def __str__(self):
        strRes = "Poliza " + str(self.idPoliza) + " " + \
                 self.descripcion + " " + str(self.fecha) + "\n"
        for m in self.colMovtos:
            strRes += str(m) + "\n"
        return strRes

class MovtoContable:
    def __init__(self,tipo,numCta,monto):
        self.tipo   = tipo
        self.numCta = numCta
        self.monto  = monto

    def __str__(self):
         strRes = "(" + self.tipo + ") " + str(self.numCta)
         if self.tipo == "A":
             strRes += " " * 12
         strRes += "     " + "{:15,.2f}".format(self.monto)
         return strRes
 
# =============================================================================
#                                Script principal
# =============================================================================

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
#    Ejercicio 1) Balance contable:
'''
     Obtener el reporte del balance contable y verificar que 
     
     "Activo = Pasivo + Capital + Ingresos - Egresos"
     
     Para ello, se debe de obtener el saldo de cada una de las partes:

         3.1)   El saldo de la Parte es un movimiento contable según la
                "naturaleza" o "tipo" de la Parte:
                 Tipo                          saldo   
               Deudora                  cargo con Suma de saldos de Ctas Deudoras - 
                                                  Suma de saldos de Ctas Acreedoras
               
               Acreedora                abono con Suma de saldos de Ctas Acreedoras - 
                                                  Suma de saldos de Ctas Deudoras

              Asimismo, el Saldo de las Cuentas Contables va de acuerdo al "tipo" de 
              Cuenta y con los movimientos de cargo y abono de la cuenta:
                 Tipo                          saldo   
               Deudora                  cargo con Suma de cargos- 
                                                  Suma de abonos
               
               Acreedora                abono con Suma de abonos - 
                                                  Suma de cargos
      
        3.2) Implemente cada uno de los saldos requeridos y agregue la salida
             en el reporte de la contabilidad.
             
'''    
# =============================================================================
#      Ejercicio 2) Estado de Resultados
'''
      Obtener un reporte con el estado de resultados:
          Ingresos - Egresos
          Reportando el saldo de cada una de las cuentas
         
'''
# =============================================================================
# =============================================================================
#      Ejercicio 3) Cierre contable
'''
    Ejecutar la operación del cierre contable.
    El cierre contable consiste en "pasar" el efecto de cada una de las 
    cuentas de Ingresos y Egresos a la cuenta de Resultado del Ejercicio y
    dejando "en ceros" las cuentas de Ingresos y Egresos.
    Para ello (desde la misma Contabilidad):
        3.1) Verificar la existencia de la cuenta 
                  300100 Resultado del Ejercicio (A))
             en caso de no existir darla de alta.
        3.2) Crear la Póliza de Cierre
        3.3) Para cada una de las cuentas de Ingresos y Egresos
             Obtener el saldo de la cuenta y agregarlo con el tipo dado por el saldo
             a la póliza de cierre a la cta 300100
             agregar a la póliza de cierre un "contra movimiento" a la misma cuenta
             de donde se obtuvo el saldo.
       3.4)  Registrar en la contabilidad la póliza de cierre.      
'''
# =============================================================================

# =============================================================================
#      Ejercicio 4) Poliza para pasivo por ISR
'''
     En caso de haber utilidad (Saldo de la cuenta 300100 es un abono) se debe
     generar una póliza con el 30% de la utilidad como adeudo a la cuenta 
                 200100 ISR por Pagar (A)
     y un cargo a la cuenta
                 300100 para disminuir la cantidad de la utilidad posterior
    al ISR.
     
'''
# =============================================================================




print(cadsep)
#print(conta.balance())
print(cadsep)

#
# ========================== FIN DEL SCRIPT PRINCIPAL =====================
