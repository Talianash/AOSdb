
# coding: utf-8

# # Описание кода
# 
# В коде задается 3 класса: организм, АТФаза и последовательность. Они все имеют постфикс "pre", птому что далее классы со схожими названиями используются при задании базы данных.
# 
# Есть и защита для строк в целом. Если в начале не стоит идентификатора, то строка пишется в переменную __broken_string__ и выводится после завершения работы.

# ### Версия 3
# Данный файл обрабатывает базу данных из файла Operons_formatted_271218.txt
# 
# 1)

# In[1]:


class Organism_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0] 
        self.field_info = list_1[1] #second part of the line, where name and id are stated
        self.warnings = [] #V2_added, to check if the organism should be added to the database
        self.name = ''
        self.strain = ''
        self.taxonomy = ''
        self.operon_num = 0 #V2_added
        self.fof1 = [] #Child atpases
        self.comment = ''
        
    def add_operon_num(self): #V2_added
        for i in self.fof1:
            self.operon_num = self.operon_num + len(i.operons)
        
    def parce(self):
        parce_l = self.field_info.strip().split()
        self.name = parce_l.pop(0) + ' ' + parce_l.pop(0)
        self.strain = ' '.join(parce_l)
        return 0


# In[2]:


class Atpase_pre(object):
    def __init__(self):
        self.type = ''
        organism = 0
        self.operons = [] #child operons
        self.subunit_names = []
        self.subunits = [] #Subunit_pre objects are added here
        self.additional_proteins = [] #
        self.field_list = ['Organism', 'Taxonomy', 'Type', 'Operon number', 'Additional_protein']
        self.subunit_list = [['alpha'], ['beta'], ['gamma'], ['delta'], ['epsilon'], ['A'], ['B', 'B1', 'B2'], ['C'], ['I2', 'I']] #V2_Changed!! I added
        


# In[3]:


class Operon(object):
    def __init__(self):
        self.atpase = 0 #parent atpase
        self.number = 0
        self.type = 'Unknown'
        self.add_prots = [] #child additional proteins
        self.subunits = [] #child subunits


# In[4]:


class Subunit_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0]
        self.field_info = list_1[1]
        self.atpase = 0 #parent atpase
        self.id = ''
        self.operon = 0 #parent operon
        self.start = -1
        self.end = -1
        self.length = -1 #V2_added!!
        self.direction = '' #V2_added!!
        self.seq = ''
        self.comment = ''
        self.field_list = ['ProtID', 'Start', 'End', 'Sequence', 'Comments', 'Length', 'Direction'] #V2_changed!! Operon field deleted, Length and Direction were added
        self.field_check = ['No', 'No', 'No', 'No', 'No', 'No', 'No']
    
    
    def parce(self):
        parce_l = self.field_info.strip().split(';')
        if parce_l[-1] == '':
            parce_l.pop(-1)
        for i in parce_l:
            pre_field = i.strip().split("-")
            field = [a.strip() for a in pre_field]
            if field[0] == 'ProtID':
                self.id = field[1]
            elif field[0] == 'Length': #V2_added!!
                self.length = int(field[1])
            elif field[0] == 'Direction': #V2_added!! VERY DIRTY SOLUTION
                if len(field) == 3:
                    self.direction = '-1'
                elif len(field) == 2:
                    self.direction = '1'
            elif field[0] == 'Start':
                self.start = int(field[1])
            elif field[0] == 'End':
                self.end = int(field[1])
            elif field[0] == 'Sequence':
                self.seq = field[1]
            elif field[0] == 'Comments':
                self.comment = field[1]

    


# In[8]:


def parce_file(file_name):
    all_field_list = ['Organism', 'Taxonomy', 'ATP synthase type', 'Operon number', 'Operon type', 'comment_on_data'] #V3_changed!! Type is changed to 'ATP synthase type', 'Operon type' added
    subunit_list = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'A', 'B', 'B1', 'B2', 'C', 'I2', 'I', 'Add_prot']
    f = open(file_name, 'r')
    broken_strings = []
    organisms = []
    broken_organisms = []
    org_name_list =[]
    for l in f:
        line = l.strip().split(':')
        if line[0] in all_field_list:
            if line[0] == 'Organism': #The most difficult: how to write info to the correct organism and fof1.
                if len(organisms) != 0:
                    organisms[-1].add_operon_num()
                    a = Organism_pre(line)
                    a.parce()
                    if a.name in org_name_list:
                        #print('It doubles')
                        #organisms[-1].fof1.append(Atpase_pre())
                        #organisms[-1].fof1[-1].organism = organisms[-1]
                        meme = 0
                    else:
                        organisms.append(a)
                        #temp = organisms[-1].parce()
                        org_name_list.append(organisms[-1].name)
                        #organisms[-1].fof1.append(Atpase_pre())
                        #organisms[-1].fof1[-1].organism = organisms[-1]
                else:
                    organisms.append(Organism_pre(line))
                    temp = organisms[-1].parce()
                    org_name_list.append(organisms[-1].name)
            elif line[0] == 'Taxonomy':
                organisms[-1].taxonomy = line[1].strip()
            elif line[0] == 'comment_on_data':
                organisms[-1].comment = line[1].strip()
            elif line[0] == 'ATP synthase type': #-------------------New ATPase
                op_num = 0
                organisms[-1].fof1.append(Atpase_pre())
                organisms[-1].fof1[-1].organism = organisms[-1]
                t = line[1].strip()
                organisms[-1].fof1[-1].type = t
            elif line[0] == 'Operon type': #-------------------------New operon
                op_num = op_num + 1
                organisms[-1].fof1[-1].operons.append(Operon())
                o = line[1].strip() #V2!
                organisms[-1].fof1[-1].operons[-1].type = o #V3
                organisms[-1].fof1[-1].operons[-1].number = op_num
                organisms[-1].fof1[-1].operons[-1].atpase = organisms[-1].fof1[-1]
        elif line[0] in subunit_list:
            if line[0] == 'Add_prot':
                organisms[-1].fof1[-1].additional_proteins.append(Subunit_pre(line))
                organisms[-1].fof1[-1].additional_proteins[-1].atpase = organisms[-1].fof1[-1]
                organisms[-1].fof1[-1].additional_proteins[-1].operon = organisms[-1].fof1[-1].operons[-1]
                organisms[-1].fof1[-1].additional_proteins[-1].parce()
                organisms[-1].fof1[-1].operons[-1].add_prots.append(Subunit_pre(line))
                organisms[-1].fof1[-1].additional_proteins[-1].atpase = organisms[-1].fof1[-1]
                organisms[-1].fof1[-1].additional_proteins[-1].operon = organisms[-1].fof1[-1].operons[-1]
                organisms[-1].fof1[-1].operons[-1].add_prots[-1].parce()
            else:
                organisms[-1].fof1[-1].subunits.append(Subunit_pre(line))
                organisms[-1].fof1[-1].subunits[-1].atpase = organisms[-1].fof1[-1]
                organisms[-1].fof1[-1].subunits[-1].operon = organisms[-1].fof1[-1].operons[-1]
                organisms[-1].fof1[-1].subunits[-1].parce()
                organisms[-1].fof1[-1].subunit_names.append(organisms[-1].fof1[-1].subunits[-1].field_type)
                organisms[-1].fof1[-1].operons[-1].subunits.append(Subunit_pre(line))
                organisms[-1].fof1[-1].operons[-1].subunits[-1].atpase = organisms[-1].fof1[-1]
                organisms[-1].fof1[-1].operons[-1].subunits[-1].operon = organisms[-1].fof1[-1].operons[-1]
                organisms[-1].fof1[-1].operons[-1].subunits[-1].parce()
        else:
            broken_strings.append(line)
    organisms[-1].add_operon_num()
    for i in broken_strings:
        if i != [''] and i != ['---------------'] and i != ['a\tb\tg\td\te\tA\tB\tB1\tB2\tC\tI\tI2'] and i[0][1:2] != '\t':
            print('Found broken string: {}'.format(i))
    f.close()
    return organisms, broken_organisms


# In[9]:


def major_check(org_list):
    good_orgs = []
    orgs_with_no_atpase = []
    bad_orgs = []
    for org in org_list:
        sm_warnings = []
        warnings = []
        if org.name == '':
            warnings.append('Name is not stated')
        if org.strain == '':
            sm_warnings.append('Strain is not stated')
        if org.taxonomy == '':
            warnings.append('Taxonomy is not stated')
        if org.operon_num == 0 and org.comment != 'No subunits found':
            warnings.append('Operon number equals 0')
        if org.fof1 == []:
            if org.comment == 'No subunits found':
                orgs_with_no_atpase.append([org, sm_warnings])
            else:
                warnings.append('No ATPases found')
        else:
            for atpase in org.fof1:
                if atpase.type == '':
                    warnings.append('ATPase has no type')
                if atpase.organism == 0:
                    warnings.append('ATPase has no parent organism')
                if len(atpase.operons) == 0:
                    warnings.append('ATPase has 0 operons')
                if atpase.subunits == []:
                    warnings.append('ATPase has no subunits')
                else:
                    for sub in atpase.subunits:
                        if sub.atpase == 0:
                            warnings.append('{}: Subunit has no parent ATPase'.format(sub.field_type))
                        if sub.id == '':
                            warnings.append('{}: Subunit has no id'.format(sub.field_type))
                        if sub.operon == 0:
                            warnings.append('{}: Subunit has no parent operon'.format(sub.field_type))
                        if sub.start == -1 or sub.end == -1 or sub.length == 0:
                            warnings.append('{}: Subunit has bad coordinates'.format(sub.field_type))
                        if sub.direction == '':
                            warnings.append('{}: Subunit direction is not stated'.format(sub.field_type))
                        if sub.seq == '':
                            warnings.append('{}: Subunit has no sequence'.format(sub.field_type))
        if warnings == []:
            good_orgs.append([org, sm_warnings])
        else:
            bad_orgs.append([org, warnings])
    f = open('log.txt', 'w')
    for i in bad_orgs:
        f.write(i[0].name + '\tbroken\t' + '. '.join(i[1])+'\n')
    for i in orgs_with_no_atpase:
        f.write(i[0].name + '\tempty\n')
    for i in good_orgs:
        if i[1] == []:
            f.write(i[0].name + '\tgood\n')
        else:
            f.write(i[0].name + '\tgood\t' + '. '.join(i[1])+'\n')
    f.close()
    return 0


                
            

