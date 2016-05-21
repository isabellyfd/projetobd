# -*- coding: utf-8 -*-
from django.core.exceptions import*
from django.shortcuts import render
from .models import *
from .forms import UploadFileForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def home(request):
	contexto = {}
	template_name = 'index.html'

	return render(request, template_name, contexto)

def inscricao(request):
	contexto = {}
	template_name = 'home.html'

	return render(request, template_name, contexto)


def login_admin(request):
	contexto = {}
	template_name = 'login.html'

	return render(request, template_name, contexto)

def logar_admin(request):
	contexto = {}
	inscritos = Inscricao.objects.all()
	total = inscritos.count()
	template_name = 'adm.html'

	try:
		if request.user.is_authenticated():
			contexto = {
				'inscritos': inscritos,
				'total': total
			}
			return render(request, template_name, contexto)
	except:
		pass	

	if request.method == 'POST':
		print('POST')
		username = request.POST['login']
		password = request.POST['senha']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				contexto = {
					'inscritos': inscritos,
					'total': total
				}
				return render(request, template_name, contexto)
			else:
				print('Usuario nao ativo')
				return render(request, 'login.html', contexto)
		else:
			print('Usuario None')
			return render(request, 'login.html', contexto)
	print('No Post')
	return render(request, 'login.html', contexto)

@login_required
def pesquisar(request):
	template_name = 'adm.html'
	contexto = {}
	areas = []
	periodos = []
	nomes = []

	if request.method == 'POST':
		area_pesquisa = request.POST['area']
		periodo_pesquisa = request.POST['periodo']
		nome_pesquisa = request.POST['nome']
		if area_pesquisa != '':
			areas = Inscricao.objects.filter(area1=area_pesquisa)
		if periodo_pesquisa != '':
			periodos = Inscricao.objects.filter(periodo=periodo_pesquisa)
		if nome_pesquisa != '':
			nomes = Inscricao.objects.filter(name=nome_pesquisa)

		contexto ={
			'areas': areas,
			'periodos': periodos,
			'nomes': nomes
		}

		return render(request, template_name, contexto)
	return redirect('logar')




def inscrever(request):
	contexto = {}

	template_name = 'home.html'

	if request.method == 'POST' and 'nome' in request.POST:
		# UPLOAD FILES
		try:
			cadastrado = Inscricao.objects.get(cpf=request.POST['cpf'])
			if cadastrado:
				messages.add_message(request, messages.ERROR, 'Este CPF ja se encontra cadastrado')
				return render(request, template_name, contexto)
		except:
			pass

		try:
			cadastrado_email = Inscricao.objects.get(email=request.POST['email'])
			if cadastrado_email:
				messages.add_message(request, messages.ERROR, 'Este e-mail ja se encontra cadastrado')
				return render(request, template_name, contexto)
		except:
			pass


		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			nova_inscricao = Inscricao()
			
			nova_inscricao.image = form.cleaned_data['foto']
			nova_inscricao.historico = form.cleaned_data['historico']
			nova_inscricao.curriculum = form.cleaned_data['curriculum']

			nova_inscricao.set_password(request.POST['senha'])
			nova_inscricao.name = request.POST['nome']
			nova_inscricao.username = request.POST['cpf']
			nova_inscricao.email = request.POST['email']
			nova_inscricao.cpf = request.POST['cpf']
			nova_inscricao.birth_data = request.POST['data-nascimento']
			nova_inscricao.curso = request.POST['curso']
			nova_inscricao.area1 = request.POST['area1']
			nova_inscricao.area2 = request.POST['area2']
			nova_inscricao.turno = request.POST['turno']
			nova_inscricao.periodo = request.POST['periodo']
			nova_inscricao.linkedin = request.POST['linkedin']

			try:
				nova_inscricao.save()
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'O nome dos seus arquivos possuem caracteres especiais(@, /, ´, ^, ~), renomeia eles e tente novamente.')
				try:
					lixo = Inscricao().objects.get(email=request.POST['email'])
					if lixo:
						lixo.delete()
				except:
					pass
				return render(request, template_name, contexto)

			messages.add_message(request, messages.SUCCESS, 'Inscricao realizada com sucesso')

	return render(request, template_name, contexto)

def editar_inscrito(request):
	contexto = {}
	template_name = 'editar-inscrito.html'

	try:
		if request.user.is_authenticated():
			contexto = {
				'inscrito': request.user
			}
			return render(request, template_name, contexto)
	except:
		pass

	if request.method == 'POST':

		cpf = request.POST['cpf_login']
		password = request.POST['senha_login']
		user = authenticate(username=cpf, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				contexto = {
					'inscrito': user
				}
				return render(request, template_name, contexto)
			else:
				return render(request, 'home.html', contexto)
		else:
			messages.add_message(request, messages.ERROR, 'Verifique os dados e tente novamente')
			return render(request, 'home.html', contexto)

	return render(request, 'home.html', contexto)

def editar_admin(request, id):
	contexto = {}
	template_name = 'editar-admin.html'

	try:
		inscrito = Inscricao.objects.get(id=id)
	except ObjectDoesNotExist:
		print('nao')
		return render(request, 'adm.html', contexto)

	contexto = {
		'inscrito': inscrito
	}

	return render(request, template_name, contexto)

@login_required
def ver_admin(request, id):
	contexto = {}
	template_name = 'ver-inscrito.html'

	try:
		inscrito = Inscricao.objects.get(id=id)
	except ObjectDoesNotExist:
		print('nao')
		return render(request, 'adm.html', contexto)

	contexto = {
		'inscrito': inscrito
	}

	return render(request, template_name, contexto)

@login_required
def enviar_email(request, id):
	
	inscrito = Inscricao.objects.get(id=id)
	nome = inscrito.name

	if inscrito.turno == 'Tarde':
		send_mail(
			'Processo Seletivo CITi - Confirmação de Inscrição.',
			"Prezado(a) " + nome + "\n" +
			"Gostariamos de agradecer o seu interesse em participar do nosso Processo Seletivo." + "\n" +
			"Você foi aprovado na avaliação de currículo/histórico escolar." + "\n" +
			"Seu próximo compromisso é comparecer a Dinâmica de Grupo em horário escolhido por você no ato de inscrição." + "\n" + "\n" +

			"Tarde - 14 as 17h" + "\n" + "\n" +

			"Contamos com você!" + "\n" +

			"Atenciosamente.",
			'contato@citi.org.br',
			['ailsoncgt@gmail.com'],
			fail_silently=True)
	else:
		send_mail(
			'Processo Seletivo CITi - Confirmação de Inscrição.',
			"Prezado(a) " + nome + "\n" +
			"Gostariamos de agradecer o seu interesse em participar do nosso Processo Seletivo." + "\n" +
			"Você foi aprovado na avaliação de currículo/histórico escolar." + "\n" +
			"Seu próximo compromisso é comparecer a Dinâmica de Grupo em horário escolhido por você no ato de inscrição." + "\n" + "\n" +

			"Tarde - 14 as 17h" + "\n" + "\n" +

			"Contamos com você!" + "\n" +

			"Atenciosamente." + "\n",
			'contato@citi.org.br',
			['ailsoncgt@gmail.com'],
			fail_silently=True)

	return redirect('logar')



def salvar_edicao(request, id):
	template_name = 'home.html'
	contexto = {}

	try:
		inscrito = Inscricao.objects.get(id=id)
	except ObjectDoesNotExist:
		print('Objeto inexistente')
		return render(request, template_name, contexto)

	if request.method == 'POST':

		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			inscrito.image = form.cleaned_data['foto']
			inscrito.historico = form.cleaned_data['historico']
			inscrito.curriculum = form.cleaned_data['curriculum']

		else:
			print('form invalido')
			try:
				inscrito.image = request.FILES['foto-editar']
			except:
				pass

			try:
				inscrito.historico = request.FILES['historico-editar']
			except:
				pass

			try:
				inscrito.curriculum = request.FILES['curriculum-editar']
			except:
				pass

		inscrito.name = request.POST['nome']
		inscrito.username = request.POST['cpf']
		inscrito.email = request.POST['email']
		inscrito.cpf = request.POST['cpf']
		inscrito.birth_data = request.POST['data-nascimento']
		inscrito.curso = request.POST['curso']
		inscrito.area1 = request.POST['area1']
		inscrito.area2 = request.POST['area2']
		inscrito.turno= request.POST['turno']
		inscrito.periodo = request.POST['periodo']
		inscrito.linkedin = request.POST['linkedin']
		try:
			inscrito.observacoes = request.POST['observacoes']
		except:
			pass

		try:
			inscrito.save()
		except Exception as e:
				messages.add_message(request, messages.ERROR, 'O nome dos seus arquivos possuem caracteres especiais(@, /, ´, ^, ~), renomeia eles e tente novamente.')
				contexto = {
					'inscrito': inscrito
				}
				if request.user.is_superuser:
					return render(request, 'editar-admin.html', contexto)
				else:
					return render(request, 'editar-inscrito.html', contexto)

		messages.add_message(request, messages.SUCCESS, 'Dados alterados com sucesso')


		print('sucesso')

		if request.user.is_superuser:
			return redirect('logar')
		else:
			logout(request)
			return redirect('inscricao')
	print('No post')
	return render(request, template_name, contexto)

def logout_admin(request):
	logout(request)
	contexto = {}

	return render(request, 'home.html', contexto)

def cadastrar_periodo(request):
	inscritos = Inscricao.objects.all()
	doisedesesseis = '2016.1'
	periodo = Periodo.objects.filter(nome=doisedesesseis)

	for inscrito in inscritos:
		if periodo:
			print (periodo)
			periodo[0].inscritos.add(inscrito)

	periodo[0].save()

	return 'Inscritos no PSC 2016.1'