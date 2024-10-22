# !pip install supabase

# ou 

# pip install supabase

import os
from datetime import datetime
import uuid
import re
from supabase import create_client, Client
supabase: Client = create_client("https://brioutndycetdzaqsxka.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyaW91dG5keWNldGR6YXFzeGthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM1NjIxNDgsImV4cCI6MjAyOTEzODE0OH0.fE2ANGfCaVLTaFZMb8d43WUEqOsCiURSL-NRjXO4ga0")

id = ''
# defino id = '', afinal, vou usa-lo como parâmetro mais tarde, então ja defino como um valor "nulo" desde já

def limparPrompt() :
    if os.name == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def listarUsuariosCadastrados(usuariosCadastrados) :
  response = supabase.table("usuarios").select("*").execute().data

  for i in range(len(response)) :
    usuariosCadastrados.append({
      'id' : response[i]['id'],
      'email' : response[i]['email'],
      'name' : response[i]['name'],
      'user_name' : response[i]['user_name'],
      'password' : response[i]['password']
        })


usuariosCadastrados = []
listarUsuariosCadastrados(usuariosCadastrados)


def verificarEmail (email) :
  validacao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
  if(re.fullmatch(validacao, email)):
   
    return True
  else:
    return False


def cadastrar() :
    # try :
        usuariosCadastrados = []
        listarUsuariosCadastrados(usuariosCadastrados)

        id = str(uuid.uuid4())
        email = input('Digite seu email: ')
        if verificarEmail(email) != True :
            print('Email inválido, tente novamente.')
            cadastrar()

        name = input('Digite seu nome completo: ')
        user_name = input('Digite seu user_name: ')

        for i in usuariosCadastrados :
            if i['email'] ==  email or i['user_name'] ==  user_name :
                print('Email ou nome de usuário já cadastrado , tente outro.')
                cadastrar()
        tamanho_user_name = len(user_name)

        if tamanho_user_name >= 40 or tamanho_user_name <= 5 :
            print('O nome de usuário deve conter entre 5 e 20 caracteres')

        password = input('Digite sua senha: ')

        if len(password) <= 6 :
            print('A senha deve conter no mínimo 6 caracteres')
            cadastrar()
        elif len(password) > 16 :
            print('A senha não pode ter mais que 16 caracteres')
            cadastrar()

        supabase.table("usuarios").insert({"id": id , "email" : email ,"name": name , "user_name":user_name , "password" :password }).execute()

        print('Usuário cadastrado com sucesso!')

    # except:
    #     print('Houve um erro\nTente novamente mais tarde')
    #     cadastrar()

def login(id) :
  try :
    user_name = input('Digite seu user name: ')
    password = input('Digite sua senha: ')
    response = supabase.table("usuarios").select("*").eq("user_name" , user_name ).eq("password" , password).execute().data

    if user_name != response[0]['user_name'] or password != response[0]['password'] :
        print('Usuário Não Cadastrado, ou senha/user name incorreta.')
        return login()

    print(response[0]['email'] , " -- " , response[0]['user_name'] , " -- Logado com sucesso")

    id = response[0]['id']
    return id
  except:
    print('Nome de usuario ou senha incorretos \nOu o usuário não foi cadastrado')

  
    

def mostrarUsuarios () :
  todosUsuarios = supabase.table("usuarios").select("*").execute().data

  for i in range (len(todosUsuarios)) :
    user = todosUsuarios[i]['user_name']
    print("(",(i+1) , ") ", user)


def comentarComUsuario () :
  usuarioId = ''
  comment = '' 
  # condição para sair da aba de comentários

  userId = login(usuarioId)

  # mostrarUsuarios()
  usuariosCadastrados = []
  listarUsuariosCadastrados(usuariosCadastrados)    

  for i in range(len(usuariosCadastrados)) :
    if userId == usuariosCadastrados[i]['id'] :
      comment_owner = usuariosCadastrados[i]['user_name']
      comment_owner_id = usuariosCadastrados[i]['id']
      print(comment_owner , ' (Eu)')
      continue
    nomeUsuario = usuariosCadastrados[i]['user_name']
    print("(",(i+1) , ") ", nomeUsuario)


  escolhaUsuarios = int(input('Escolha um usuario para conversar: '))
  limparPrompt()
  
  print("Digite 'sair' quando quiser sair da aba de comentários!")
  while comment != 'sair' :
    for i in range(len(usuariosCadastrados)) :
      if escolhaUsuarios == (i + 1) and comment_owner == usuariosCadastrados[i]['user_name']:
        print('Você não pode escolher a sí mesmo')
        comentarComUsuario ()

      if escolhaUsuarios == (i+1) :
        other_user = usuariosCadastrados[i]['id']
        comentarioUsuario = supabase.table('comentarios').select('*').eq('other_user' , other_user).eq('comment_owner' , comment_owner).order().execute().data
        # aqui, a gente pega os comentários que o usuario atual fez, usando como parâmetro o nome do outro usuário (só pode ser 1) e o nome de quem digitou (só pode ser 1)


        comentarioUsuarioResposta = supabase.table('comentarios').select('*').eq('other_user' , comment_owner_id).eq('comment_owner' , usuariosCadastrados[i]['user_name']).execute().data
        # para liga-los, a gente pega os comentários do outro usuário, usando o seu o id do outro usuário como parâmetro (só pode ter 1 conversa entre os 2) e o próprio nome (tem que ser único também)
        
        print("(",usuariosCadastrados[i]['user_name'] , ")")
        for i in comentarioUsuario :
          print(i['comment_owner'] , ' :',i['comment'])
        for i in comentarioUsuarioResposta :
          print(i['comment_owner'] , ' :',i['comment'])

        id = str(uuid.uuid4())
        comment = input('Deixe seu comentário: ')  

        if comment == 'sair' :
          comentarComUsuario()
          break


        commented_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        supabase.table("comentarios").insert({"id": id , "comment_owner" : comment_owner , "comment" : comment , "commented_at" : commented_at , "other_user" : other_user}).execute()
        limparPrompt()

def menu () :
    print('1: Cadastrar')
    print('2: Conversar com usuario (Login necessário)')
    print('3: Sair')

    opcao = int(input('Escolha uma opção: '))
    return opcao


def run () :
  limparPrompt()
  while True:
    # try
      match menu():
        case 1:
          print('Cadastrando...')
          cadastrar()
          limparPrompt()
          run()

        case 2:
          limparPrompt()
          comentarComUsuario()

        case 3:
          print('Saindo... Espero ve-lo em breve!')
          id = ''
          limparPrompt()
          break
          
          
        case _:
          print('Opção inválida')
          continue

    # except:
    #   print('Tente novamente')

run()