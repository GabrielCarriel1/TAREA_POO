import datetime
import json
import os
import time
import msvcrt  
import datetime
from abc import ABC
from colorama import init, Fore, Style
from functools import reduce
from company import Company
from components import Menu, Valida
from customer import RegularClient, JsonFile
from iCrud import ICrud
from product import Product
from sales import Sale
from utilities import borrarPantalla, gotoxy
from utilities import reset_color, red_color, green_color, blue_color, purple_color

path, _ = os.path.split(os.path.abspath(__file__))


def saveClient(dni, first_name, last_name, valor, json_file):
  client = {
    "dni": dni,
    "first_name": first_name,
    "last_name": last_name,
    "valor": valor
  }

  old_data = json_file.read()
  if old_data is not None:
    old_clients = json.loads(old_data)
  else:
    old_clients = []

  old_clients.append(client)

  json_file.write(json.dumps(old_clients))
  
def saveProduct(id, descripcion, precio, stock, json_file):
  product = {
    "id": id,
    "descripcion": descripcion,
    "precio": precio,
    "stock": stock
  }

  old_data_products = json_file.read()
  if old_data_products is not None:
    old_products = json.loads(old_data_products)
  else:
    old_products = []

  old_products.append(product)

  json_file.write(json.dumps(old_products))

def validate_input(prompt, condition, error_message):
    while True:
        user_input = input(prompt).strip()
        if condition(user_input):
            return user_input
        else:
            print("\033[91m\033[4m" + error_message + "\033[0m")
            time.sleep(2)

def print_message(message):
    print("\033[97m\033[1m\033[4m" + message + "\033[0m")

class CrudClients(ICrud, ABC):
  def create(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print("\n Registrando Cliente")
        dni = validate_input("Ingresar cédula : ", lambda x: len(x) == 10 and x.isdigit() and ' ' not in x, "Cédula inválida")

        first_name = validate_input("Ingresar nombres : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and len(x.split()) == 2, "Nombres mal tipados")

        last_name = validate_input("Ingresar apellidos : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and len(x.split()) == 2, "Apellidos mal tipados")

        cliente = input("Usted es cliente regular o VIP? (regular/vip) : ").lower()

        if cliente == "regular":
            valor = 0.10
            valor = round(valor, 2)  
        elif cliente == "vip":
            limite_vip = float(input("Ingresar el límite VIP del cliente : "))
            if limite_vip > 20000:
                limite_vip = 10000
            elif limite_vip < 10000:
                limite_vip = 10000
            else:
                limite_vip = round(limite_vip, 2)  
            valor = limite_vip

        borrarPantalla()
        print_message("Datos")
        smsCliente = input("Usted es cliente regular o VIP? (regular/vip) : ").lower()
        if smsCliente == "regular":
            print(
            f" DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Descuento por ser regular cliente : {valor}")
            if input(" Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                saveClient(dni, first_name, last_name, valor, json_file)
                print_message("Cliente se guardó.")
                time.sleep(2)
            else:
                print_message("Cliente no se guardó.")
                time.sleep(2)
            break
        elif cliente == "vip":
            print(
            f"DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Límite de crédito : {valor}")
            if input("Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                saveClient(dni, first_name, last_name, valor, json_file)
                print_message("Cliente se guardó.")
                time.sleep(2)
            else:
                print_message("Cliente no se guardó.")
                time.sleep(2)
            break
        
  def update(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        dni = validate_input("Ingresar cédula, para actualizar datos del cliente : ", lambda x: len(x) == 10 and x.isdigit() and ' ' not in x, "Cédula inválida")

        old_clients = json.loads(json_file.read() or '[]')

        for client in old_clients:
            if client["dni"] == dni:
                while True:
                    borrarPantalla()
                    print_message("Actualizando cliente.")
                    print()
                    dni = validate_input(" Ingresar número de cédula : ", lambda x: len(x) == 10 and x.isdigit() and ' ' not in x, "Cédula inválida")

                    first_name = validate_input(" Ingresar nombres : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and len(x.split()) == 2 and all(len(name) >= 3 for name in x.split()), "Nombres mal tipados")

                    last_name = validate_input(" Ingresar apellidos : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and len(x.split()) == 2 and all(len(name) >= 3 for name in x.split()), "Apellidos mal tipados")

                    cliente = input(" Usted es cliente regular o VIP? (regular/vip) : ").lower()

                    if cliente == "regular":
                        valor = 0.10
                        valor = round(valor, 2)  
                    elif cliente == "vip":
                        limite_vip = float(input(" Ingresar el límite VIP del cliente : "))
                        if limite_vip > 20000:
                            limite_vip = 10000
                        elif limite_vip < 10000:
                            limite_vip = 10000
                        else:
                            limite_vip = round(limite_vip, 2) 
                        valor = limite_vip

                    borrarPantalla()
                    print_message("\n Datos")
                    if cliente == "regular":
                        print(
                            f" DNI : {dni} \n Nombres : {first_name}\n Apellidos : {last_name}\n Descuento por ser cliente regular : {valor}")
                    elif cliente == "vip":
                        print(
                            f"DNI : {dni} \nNombres : {first_name}\nApellidos : {last_name}\nLímite de crédito VIP : {valor}")

                    if input("Guardar yes o no ? (YES/NO) : ").lower() == 'yes':
                        client["dni"] = dni
                        client["first_name"] = first_name
                        client["last_name"] = last_name
                        client["valor"] = float(valor)
                        json_file.write(json.dumps(old_clients))
                        print_message("Cliente actualizado.")
                        time.sleep(2)
                        break
                    else:
                        print_message("Cancelada.")
                        time.sleep(2)
                        break

        else:
            print("\033[91mCliente no encontrado\033[0m")
            
        break

  def delete(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print_message("\n Eliminará datos del cliente.")
        dni = validate_input("Ingresar cédula : ", lambda x: len(x) == 10 and x.isdigit() and ' ' not in x, "Cédula inválida")

        old_clients = json.loads(json_file.read() or "[]")

        updated_clients = [client for client in old_clients if client["dni"] != dni]
        deleted = len(updated_clients) != len(old_clients)

        if deleted:
            borrarPantalla()
            print_message("Verificar Datos")
            print()
            client_to_delete = next((client for client in old_clients if client["dni"] == dni), None)
            print("DNI:", dni)
            print("Nombres:", client_to_delete["first_name"])
            print("Apellidos:", client_to_delete["last_name"])
            print("Crédito:", client_to_delete["valor"])
            aceptar = input("Eliminar cliente. ? (YES/NO)").lower()

            if aceptar == 'yes':
                print_message("Cliente eliminado.")
                json_file.write(json.dumps(updated_clients))
                time.sleep(2)
                
            else:
                print_message("Cancelada.")
                time.sleep(2)
        else:
            print("\nCliente no existe.")
            time.sleep(2)
            continue
        break
        
  def consult(self):
    json_file_path = path + '/archivos/clients.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print_message("Consultar cliente.")
        print()
        dni = validate_input("Ingresar cédula : ", lambda x: len(x) == 10 and x.isdigit() and ' ' not in x, "Cédula inválida")

        old_clients = json.loads(json_file.read() or "[]")

        if not old_clients:
            print("Datos del json vacío")
            return

        found_clients = [client for client in old_clients if client["dni"] == dni]
        if found_clients:
            borrarPantalla()
            print_message("\n Consultando cliente")
            print("\n" + "DNI".ljust(30) + "Nombres".ljust(30) + "Apellido".ljust(30) + "LÍMITE DEL CRÉDITO")
            for client in found_clients:
                print(str(client["dni"]).ljust(30), (client["first_name"]).ljust(30),
                      client["last_name"].ljust(30), client["valor"])
                time.sleep(2)
                input("-")
        else:
            print("Cliente no existe.")
            time.sleep(2)
            continue
            
        break


class CrudProducts(ICrud):
  def create(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print_message("\n Registrando datos del producto.")
        id = validate_input("Ingresar id del producto : ", lambda x: len(x) == 1 and x.isdigit() and ' ' not in x, "ID inválido")

        descripcion = validate_input("Ingresar descripción del producto : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and all(len(descrip) >= 3 for descrip in x.split()), "Descripción inválida")

        precio = validate_input("Ingresar precio del producto : ", lambda x: x.replace('.', '', 1).replace('-', '', 1).isdigit() and float(x) >= 0, "Precio inválido")

        stock = validate_input("Ingresar el stock del producto : ", lambda x: x.replace('.', '', 1).replace('-', '', 1).isdigit() and int(x) >= 0, "Stock inválido")

        precio = float(precio)
        stock = int(stock)

        borrarPantalla()
        print_message("\n Verificar Datos")
        print()
        print(f"ID : {id}\n Descripción : {descripcion}\n Precio $ : {precio}\n Stock : {stock}")
        if input("Guardar producto ? (YES/NO) : ").lower() == 'yes':
            saveProduct(id, descripcion, precio, stock, json_file)
            print_message("Producto guardado.")
            time.sleep(2)
        else:
            print_message("No guardado.")
            time.sleep(2)

        break

  def update(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Actualizar producto.')
        print()
        id = validate_input("Ingresar id del producto : ", lambda x: len(x) == 1 and x.isdigit() and ' ' not in x, "ID inválido")

        old_products = json.loads(json_file.read() or '[]')

        for product in old_products:
            if product["id"] == id:
                while True:
                    borrarPantalla()
                    print('Actualizando datos del producto.')
                    id = validate_input("Ingresar id del producto : ", lambda x: len(x) == 1 and x.isdigit() and ' ' not in x, "ID inválido")

                    descripcion = validate_input("Ingresar descripción del producto : ", lambda x: all(c.isalpha() or c.isspace() for c in x) and all(len(descrip) >= 3 for descrip in x.split()), "Descripción inválida")

                    precio = validate_input("Ingresar precio del producto : ", lambda x: x.replace('.', '', 1).replace('-', '', 1).isdigit() and float(x) >= 0, "Precio inválido")

                    stock = validate_input("Ingresar el stock del producto : ", lambda x: x.replace('.', '', 1).replace('-', '', 1).isdigit() and int(x) >= 0, "Stock inválido")

                    precio = float(precio)
                    stock = int(stock)

                    borrarPantalla()
                    print("\nVerificar Datos")
                    print(f"ID : {id}\nDescripción : {descripcion}\nPrecio $ : {precio}\nStock : {stock}")
                    aceptar = input("Aceptar la actualizacion (YES/NO)").lower()

                    if aceptar == 'yes':
                        product["id"] = id
                        product["descripcion"] = descripcion
                        product["precio"] = precio
                        product["stock"] = stock
                        json_file.write(json.dumps(old_products))
                        print("Producto actualizado.")
                        time.sleep(2)
                        return
                    else:
                        print("Cancelado.")
                        time.sleep(2)

                    break

        print("Producto no encontrado.")
        time.sleep(2)

  def delete(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Eliminará producto.')
        print()
        id = validate_input("Ingresar id del producto : ", lambda x: len(x) == 1 and x.isdigit() and ' ' not in x, "ID inválido")

        old_products = json.loads(json_file.read() or '[]')

        updated_products = [product for product in old_products if product["id"] != id]
        deleted = len(updated_products) != len(old_products)

        if deleted:
            borrarPantalla()
            print("\n Verificar Datos")
            product_to_delete = next((product for product in old_products if product["id"] == id), None)
            print("ID :", id)
            print("Descripción :", product_to_delete["descripcion"])
            print("Precio :", product_to_delete["precio"])
            print("Stock :", product_to_delete["stock"])
            aceptar = input("Eliminar producto. ? (YES/NO) : ").lower()

            if aceptar == 'yes':
                print("Producto eliminado.")
                json_file.write(json.dumps(updated_products))
                time.sleep(2)
            else:
                print("Cancelada.")
                time.sleep(2)
        else:
            print("Producto no encontrado.")
            time.sleep(2)

        break

  def consult(self):
    json_file_path = path + '/archivos/products.json'
    json_file = JsonFile(json_file_path)

    while True:
        borrarPantalla()
        print('Consultar producto.')
        print()
        id = validate_input("Ingresar id del producto : ", lambda x: len(x) == 1 and x.isdigit() and ' ' not in x, "ID inválido")

        old_products = json.loads(json_file.read() or '[]')

        if not old_products:
            print("Json sin datos")
            return

        found_product = [product for product in old_products if product["id"] == id]
        if found_product:
            borrarPantalla()
            print("\n Consultando Datos")
            print("\n" + "ID".ljust(30) + "Descripción".ljust(30) + "Precio".ljust(30) + "Stock")
            for product in found_product:
                id_str = str(product["id"]).ljust(30)
                descripcion_str = str(product["descripcion"]).ljust(30)
                precio_str = str(product["precio"]).ljust(30)
                stock_str = str(product["stock"])
                print(id_str, descripcion_str, precio_str, stock_str)
                time.sleep(3)
                input("\nesc___")
        else:
            print("No existe producto.")
            time.sleep(2)
            continue

        break


class CrudSales(ICrud):
  def create(self):
    validar = Valida()
    borrarPantalla()
    print('\033c', end='')
    gotoxy(2,1);print(green_color+"██"*50+reset_color)
    gotoxy(30,2);print(blue_color+"Registro de Venta")
    gotoxy(17,3);print(blue_color+Company.get_business_name())
    gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
    gotoxy(66,4);print(" Subtotal:")
    gotoxy(66,5);print(" Decuento:")
    gotoxy(66,6);print(" Iva     :")
    gotoxy(66,7);print(" Total   :")
    gotoxy(10,6);print("Cedula:")
    dni = validar.solo_numeros("Error: Solo numeros",23,6)
    
    json_file = JsonFile(path+'/archivos/clients.json')
    clients_data = json_file.find("dni", dni)
    if not clients_data:
        gotoxy(35,6);print("Cliente no existe")
        return
    client = clients_data[0]
    cli = RegularClient(client["first_name"], client["last_name"], client["dni"], card=True) 
    sale = Sale(cli)
    gotoxy(35,6);print(cli.fullName())
    gotoxy(2,8);print(green_color+"██"*50+reset_color) 
    gotoxy(5,9);print(purple_color+"Linea") 
    gotoxy(12,9);print("Id_Articulo") 
    gotoxy(24,9);print("Descripcion") 
    gotoxy(38,9);print("Precio") 
    gotoxy(48,9);print("Cantidad") 
    gotoxy(58,9);print("Subtotal") 
    gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
    
    follow = "s"
    line = 1
    while follow.lower() == "s":
        gotoxy(7,9+line);print(line)
        gotoxy(15,9+line);id_articulo = validar.solo_numeros("Error: Solo numeros",15,9+line)
        
        json_file = JsonFile(path+'/archivos/products.json')
        prods = json_file.find("id", id_articulo)
        if not prods:
            gotoxy(24,9+line);print("Producto no existe")
            time.sleep(1)
            gotoxy(24,9+line);print(" "*20)
        else:    
            prods = prods[0]
            product = Product(prods["id"], prods["descripcion"], prods["precio"], prods["stock"])
            gotoxy(24,9+line);print(product.descrip)
            gotoxy(38,9+line);print(product.preci)
            gotoxy(49,9+line);qty = int(validar.solo_numeros("Error: Solo numeros",49,9+line))
            gotoxy(59,9+line);print(product.preci * qty)
            sale.add_detail(product, qty)
            gotoxy(76,4);print(round(sale.subtotal,2))
            gotoxy(76,5);print(round(sale.discount,2))
            gotoxy(76,6);print(round(sale.iva,2))
            gotoxy(76,7);print(round(sale.total,2))
            gotoxy(74,9+line);follow = input() or "s"  
            gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
            line += 1
    
    gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
    gotoxy(54,9+line);procesar = input().lower()
    if procesar == "s":
        gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        if invoices:
            invoices = json.loads(invoices) 
            ult_invoices = invoices[-1]["factura"] + 1
        else:
            ult_invoices = 1

        json_file = JsonFile(path+'/archivos/invoices.json')
        data = sale.getJson()
        data["factura"] = ult_invoices
        json_file.append(data)

    else:
        gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
    time.sleep(2)

  def update(self):
    while True:
        borrarPantalla()
        print('Actualizar datos de la factura.')
        print()
        fact = input("Ingresar número de factura, para actualizar los datos :").strip()
        if ' ' in fact or not fact.isdigit() or len(fact) != 1:
            print("Numero de factura incorrecto.")
            time.sleep(2)
            continue
    
        fact = float(fact)
        json_file = JsonFile(path+'/archivos/invoices.json')
        clients_data = json_file.find("factura", fact)

        if clients_data:
            factura_encontrada = clients_data[0]  
            
            print("Cliente  : ", factura_encontrada["cliente"])
            print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{factura_encontrada['Fecha']}")
            print("Subtotal : ", factura_encontrada["subtotal"])
            print("Descuento: ", factura_encontrada["descuento"])
            print("IVA      : ", factura_encontrada["iva"])
            print("Total    : ", factura_encontrada["total"])
          
            print()            
            input("\033[1m\033[4m\033[97mEnter seguir \033[0m\033[1m\033[4m\033[97mdatos a actualizar ❗\033[0m")

            validar = Valida()
            borrarPantalla()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"██"*50+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Venta")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(5,4);print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{datetime.datetime.now()}")
            gotoxy(66,4);print(" Subtotal:")
            gotoxy(66,5);print(" Descuento:")
            gotoxy(66,6);print(" IVA     :")
            gotoxy(66,7);print(" Total   :")
            gotoxy(10,6);print("Cedula:")
            dni = validar.solo_numeros("Error: Solo numeros",23,6)

            json_file = JsonFile(path+'/archivos/clients.json')
            clients_data = json_file.find("dni", dni)
            if not clients_data:
                gotoxy(35,6);print("Cliente no existe")
                return
            client = clients_data[0]
            cli = RegularClient(client["first_name"], client["last_name"], client["dni"], card=True) 
            sale = Sale(cli)
            gotoxy(35,6);print(cli.fullName())
            gotoxy(2,8);print(green_color+"██"*50+reset_color) 
            gotoxy(5,9);print(purple_color+"Linea") 
            gotoxy(12,9);print("Id_Articulo") 
            gotoxy(24,9);print("Descripcion") 
            gotoxy(38,9);print("Precio") 
            gotoxy(48,9);print("Cantidad") 
            gotoxy(58,9);print("Subtotal") 
            gotoxy(70,9);print("n->Terminar Venta)"+reset_color)

            follow = "s"
            line = 1
            while follow.lower() == "s":
                gotoxy(7,9+line);print(line)
                gotoxy(15,9+line);id_articulo = validar.solo_numeros("Error: Solo numeros",15,9+line)
                json_file_path = path + '/archivos/products.json'
                json_file = JsonFile(json_file_path)
                prods = json_file.find("id", id_articulo)
                if not prods:
                    gotoxy(24,9+line);print("Producto no existe")
                    time.sleep(1)
                    gotoxy(24,9+line);print(" "*20)
                    continue

                prods = prods[0]
                product = Product(prods["id"], prods["descripcion"], prods["precio"], prods["stock"])

                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)

                qty = int(validar.solo_numeros("Error: Solo numeros",49,9+line))

                gotoxy(59,9+line);print(product.preci * qty)

                sale.add_detail(product, qty)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))

                factura_encontrada["detalle"][0]["poducto"] = product.descrip
                factura_encontrada["detalle"][0]["precio"] = product.preci
                factura_encontrada["detalle"][0]["cantidad"] = qty

                gotoxy(74,9+line);follow = input() or "s"
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)
                line += 1

            gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
            gotoxy(54,9+line);procesar = input().lower()
            if procesar == "s":
                gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()
                if invoices:
                    invoices = json.loads(invoices)  
                    for factura in invoices:
                        if factura["factura"] == fact:
                            factura["Fecha"] = datetime.datetime.now().strftime("%Y-%m-%d") 
                            factura["cliente"] = cli.fullName()  
                            factura["subtotal"] = sale.subtotal  
                            factura["descuento"] = sale.discount  
                            factura["iva"] = sale.iva 
                            factura["total"] = sale.total  
                            factura["detalle"] = factura_encontrada["detalle"] 
                            break
                else:
                    invoices = []

                json_file.write(json.dumps(invoices, indent=4))
            else:
                gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
            time.sleep(2)
            input("enter")
        else:
            input("Factura no encontrada, presione enter")

        break

  def delete(self):
        while True:
            borrarPantalla()
            print('Actualizar datos de la factura.')
            fact = input("Ingresar número de factura, para actualizar los datos :").strip()
            if ' ' in fact or not fact.isdigit() or len(fact) != 1:
                print("numero de factura invalido.")
                time.sleep(2)
                continue
            fact = float(fact)
            json_file = JsonFile(path+'/archivos/invoices.json')
            clients_data = json_file.find("factura", fact)
            if not clients_data:
                print("\033[91m\033[4mno se encontro factura.\033[0m")
                time.sleep(2)
                continue
            
            factura_encontrada = clients_data[0]
            print()
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"██"*50+reset_color)
            gotoxy(30,2);print(blue_color+"Registro de Venta")
            gotoxy(17,3);print(blue_color+Company.get_business_name())
            gotoxy(5,4);print(f"Factura#: {factura_encontrada['factura']} {' '*3} Fecha:{factura_encontrada['Fecha']}")
            gotoxy(66,4);print(" Subtotal: ", factura_encontrada["subtotal"])
            gotoxy(66,5);print(" Descuento: ", factura_encontrada["descuento"])
            gotoxy(66,6);print(" IVA     : ", factura_encontrada["iva"])
            gotoxy(66,7);print(" Total   : ", factura_encontrada["total"])
            gotoxy(10,6);print("Cliente: ", factura_encontrada["cliente"])
            gotoxy(2,8);print(green_color+"██"*50+reset_color)
            print()
            print(" enter o  esc")

            while True:
                if msvcrt.kbhit():
                    entrada = msvcrt.getch()
                    if entrada == b"\x1b":
                        print()
                        print("\033[91;4m cancelada.\033[0m")
                        time.sleep(1)
                        break

                    elif entrada == b"\r":
                        fact = float(fact)
                        json_file_path = path + '/archivos/invoices.json'
                        with open(json_file_path, 'r+') as file:
                            invoices = json.load(file)
                            for i, factura in enumerate(invoices):
                                if factura["factura"] == fact:
                                    del invoices[i]
                            file.seek(0)
                            json.dump(invoices, file, indent=4)
                            file.truncate()
                        break
            break
                                
        
  def consult(self):
    
    while True:
        borrarPantalla()
        print('Consultar factura.')
        print()
        invoice = input("Ingresar número de factura, para encontrar :").strip()
        if ' ' in invoice or not invoice.isdigit() or len(invoice) != 1:
            print("Didite correctamente numero de la factura.")
            time.sleep(2)
            continue
          
        borrarPantalla()
        print('Consultando factura.')
        print()
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            if invoices:
                for fac in invoices:
                    for key, value in fac.items():
                        print(f"{key}: {value}")
                        
                    print(f"{'-' * 50}")
            else:
                print("La factura no existe.")
        else:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                for key, value in fac.items():
                    print(f"{key}: {value}")
                print(f"{'-' * 80}")

        input(f"Enter para continuar :")
        
        break

opc = ''
while opc != '4':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion", [" 1) Clientes", " 2) Productos", " 3) Ventas", " 4) Salir"], 20, 10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            menu_clients = Menu("Menu Clientes", [" 1) Ingresar", " 2) Actualizar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 10, 10)
            opc1 = menu_clients.menu()

            if opc1 == "1":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.create()

            elif opc1 == "2":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.update()

            elif opc1 == "3":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.delete()
                break
                    

            elif opc1 == "4":
                borrarPantalla()
                crud_clients = CrudClients()
                crud_clients.consult()
                     
    elif opc == "2":
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            menu_products = Menu("Menu Productos", [" 1) Ingresar", " 2) Actualizar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 20, 10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.create()

            elif opc2 == "2":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.update()
                
            elif opc2 == "3":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.delete()
                   

            elif opc2 == "4":
                borrarPantalla()
                crud_productos = CrudProducts()
                crud_productos.consult()
                          
    elif opc == "3":
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas", [" 1) Registro Venta", " 2) Modificar", " 3) Eliminar", " 4) Consultar", " 5) Salir"], 20, 10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                borrarPantalla()
                sales.create()
                  
            elif opc3 == "2":
                borrarPantalla()
                sales.update()
                           
            elif opc3 == "3":
                borrarPantalla()
                sales.delete()
                           
            elif opc3 == "4":
                borrarPantalla()
                sales.consult()
                        
        print("Regresando al menú Principal...")
        time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()