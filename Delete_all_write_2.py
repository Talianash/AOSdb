
# coding: utf-8

# In[20]:


from app import db, models
from app.models import Organism, ATPase, Operon, Sequence
    


# In[21]:


def clean_db():
    from app import db, models
    from app.models import Organism, ATPase, Operon, Sequence
    for i in Organism.query.all():
        db.session.delete(i)
    db.session.commit()
    for k in ATPase.query.all():
        db.session.delete(k)
    db.session.commit()
    for j in Operon.query.all():
        db.session.delete(j)
    db.session.commit()
    for n in Sequence.query.all():
        db.session.delete(n)
    db.session.commit()

clean_db()


# In[18]:


import Parse_input_data_v3
organism_list, btoken_list = Parse_input_data_v3.parce_file('data_input/Operons_formatted_nov_3_291218.txt')

for i in organism_list:
    organism = Organism(name = i.name, strain = i.strain, taxonomy = i.taxonomy, org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = i.operon_num, org_comment = i.comment)
    db.session.add(organism)
    db.session.commit()
    for k in i.fof1:
        print(", ".join(k.subunit_names))
        atpase = ATPase(source = i.name, fof1_type = k.type, organism = organism)
        db.session.add(atpase)
        db.session.commit()
        for j in k.operons:
            sub_li = []    
            for sub in j.subunits:
                sub_li.append(sub.field_type)
            operon = 0
            operon = Operon(operon_type = j.type, operon_number = j.number, subunit_list = ", ".join(sub_li), enzyme = atpase, organism = organism)
            db.session.add(operon)
            db.session.commit()
            for h in j.subunits:
                subunit = Sequence(subunit_name = h.field_type, subunit_id_ncbi = h.id, sequence = h.seq, start = h.start, stop = h.end, seq_comment = h.comment, operon = operon)
                db.session.add(subunit)
                db.session.commit()
db.session.commit()




# In[19]:


Sequence.query.all()

