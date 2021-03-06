#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import calc

from pprint import pprint

def is_printing(char):
	i = "qertyuioplkjhgfdsazxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM".find(char)
	if i == -1:
		return 0
	return 1

def is_tabu(string):
	for i in string:
		if i != '\t' and i != ' ':
			return 0
	return 1

def is_space(string):
	for i in string:
		if i != ' ':
			return 0
	return 1

def init_table():
	table = []
	try:
		oui = sys.argv[1]
	except:
		print "file"
		sys.exit()

	try:
		text = open(sys.argv[1], "r")
		text = text.read()
		text = text.replace("\t","")
		text = text.split('\n')
	except:
		print 'error open'
		sys.exit()

	count = 0
	for i in text:
		try:
			sharp = i.index("#")
			i = i[:sharp]
			if len(i) == 0 and is_tabu(i):
				continue
			i = ' '.join(i.split())
			table.append(i)
		except:
			if len(i) != 0 and is_tabu(i) == 0:
				i = ' '.join(i.split())
				table.append(i)
		count += 1
	return table


def interactive_input():
	string = "oui"
	text = ""
	table = []
	while(string != ""):
		string = raw_input()
		text += string + '\n'

	text = text.replace("\t","")
	text = text.split('\n')

	count = 0
	for i in text:
		try:
			sharp = i.index("#")
			i = i[:sharp]
			if len(i) == 0 and is_tabu(i):
				continue
			i = ' '.join(i.split())
			table.append(i)
		except:
			if len(i) != 0 and is_tabu(i) == 0:
				i = ' '.join(i.split())
				table.append(i)
		count += 1
	return table




def set_true_value(table):
	true_value = []
	count = 0;
	for i in table:
		if i[0] == '=':
			table.remove(i)
			i = i [ 1:]
			if(i == ''):
				return []
			i = i.split(',');
			for val in i:
				if('!' in val or '(' in val or ')' in val or '+' in val or '^' in val or '|' in val or ' ' in val or len(val) == 0):
					print 'error ='
					sys.exit()
				if((val in true_value) == False):
					true_value.append(val)
			count = 1;
	if count == 0:
		print "erreur = not found"
		sys.exit()
	return true_value

def set_chr_value(table):
	true_value = []
	count = 0;
	for i in table:
		if i[0] == '?':
			table.remove(i)
			i = i [ 1:]
			if(i == ''):
				print "error ? "
				sys.exit()
			i = i.split(',');
			for val in i:
				if('!' in val or '(' in val or ')' in val or '+' in val or '^' in val or '|' in val or ' ' in val or len(val) == 0):
					print 'error ?'
					sys.exit()
				if((val in true_value) == False):
					true_value.append(val)
			count = 1;
	if count == 0:
		print "erreur ? not found"
		sys.exit()
	return true_value


def parsing_corp_core(true_value, split, false_value):
	split = ' '.join(split.split())
	condition = split.split(' ');
	count = 0
	#print condition;
	for verif in condition:
		if(',' in verif):
			print 'erreur parsing'
			sys.exit()
		if verif == '':
			continue

		if(count % 2 == 0):
			while(verif[0] == '!' or verif[0] == '('):
				verif = verif [ 1:]
				if(len(verif) == 0):
					print "error parsing"
					sys.exit()
			while(len(verif) >= 1 and verif[len(verif) - 1] == ')'):
				verif = verif [:len(verif)-1]
			if (verif in true_value) == False  and (verif in false_value) == False :
				if('(' in verif or ')' in verif or '+' in verif or '^' in verif or '|' in verif or ' ' in verif or len(verif) == 0):
					print 'error var'
					sys.exit()
				false_value.append(verif)

		else:
			if verif != '+' and verif != '|' and verif != '^' and verif != '':
				print "erreur parsing"
				sys.exit()
		count += 1
	return (false_value);



def parsing_corp(table, true_value):
	false_value = []
	for i in table:
		split = i.split("<=>")
		if(len(split) == 1):
			split = i.split("=>")
		if len(split) == 1:
			print "erreur parsing =>"
			sys.exit()
		false_value = parsing_corp_core(true_value, split[0], false_value)
		false_value = parsing_corp_core(true_value, split[1], false_value)
	return (false_value);





def braket(tab):
	for var in tab:
		var = var.split("=>")
		if(var[0].count('(') != var[0].count(')') or var[1].count('(') != var[1].count(')')):
			print "error braket"
			sys.exit()



def false_char_in_chr(chr_value, false_value,true_value):
	for i in chr_value:
		if ((i in false_value) == False and (i in true_value) == False):
			false_value.append(i)
	return(false_value)


def double_verif(tab, i):
	new_tab = []
	y = 0
	while(y < i):
		new_tab.append(tab[y])
		y+=1
	tab[i] = tab[i].replace("<=>", "=>")
	expresion = tab[i].split("=>")
	new_tab.append(expresion[1] + ' => ' + expresion[0])
	while(y < len(tab)):
		new_tab.append(tab[y])
		y+=1

	return(new_tab)


def format(tab):
	i = 0
	if(('false' in true_value) == True or ('true' in true_value) == True or ('false' in false_char) == True or ('true' in false_char) == True):
		print 'forbident name of variable true ou false'
		sys.exit()
	while(i < len(tab)):
		tab[i] = tab[i].replace("!", " ! ")
		tab[i] = tab[i].replace("(", " ( ")
		tab[i] = tab[i].replace(")", " ) ")
		if(tab[i].count("<=>") == 1):
			tab = double_verif(tab, i)
			i -= 1
			#tab[i] = tab[i].replace("<=>", " = ")
		elif (tab[i].count("=>") == 1):
			tab[i] = tab[i].replace("=>", " > ")
		else:
			print "error"
			sys.exit()

		tab[i] = ' '.join(tab[i].split())
		i += 1
	return(tab)


if ( __name__ == "__main__"):
	verbos = False
	if('-v' in sys.argv):
		verbos = True
		sys.argv.remove('-v')


	if(len(sys.argv) == 1):
		table = interactive_input();
	else:
		table = init_table()
	true_value = set_true_value(table)
	chr_value = set_chr_value(table)
	false_char = parsing_corp(table, true_value)
	false_char = false_char_in_chr(chr_value, false_char, true_value)
	braket(table)
	table = format(table)


	#print text
	#inferences.solve(table, true_value,false_char, chr_value)
	calc.main(true_value, false_char, chr_value, table, verbos)