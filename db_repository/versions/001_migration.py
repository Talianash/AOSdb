from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
operon = Table('operon', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('operon_type', String(length=50), default=ColumnDefault('not_stated')),
    Column('operon_number', Integer),
    Column('subunit_list', String(length=200)),
    Column('add_prot_list', String(length=200), default=ColumnDefault('')),
    Column('atpase_id', Integer),
    Column('organism_id', Integer),
)

atpases = Table('atpases', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('source', String),
    Column('fof1_type', String),
    Column('subunit_list', String),
    Column('add_prot_list', String),
    Column('organism_id', Integer),
)

organisms = Table('organisms', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('org_id_ncbi', String),
    Column('taxonomy', String),
    Column('org_type', String),
    Column('fof1_number', Integer),
    Column('operon_number', Integer),
    Column('org_comment', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['operon'].columns['operon_number'].create()
    post_meta.tables['operon'].columns['subunit_list'].create()
    pre_meta.tables['atpases'].columns['add_prot_list'].drop()
    pre_meta.tables['atpases'].columns['subunit_list'].drop()
    pre_meta.tables['organisms'].columns['org_id_ncbi'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['operon'].columns['operon_number'].drop()
    post_meta.tables['operon'].columns['subunit_list'].drop()
    pre_meta.tables['atpases'].columns['add_prot_list'].create()
    pre_meta.tables['atpases'].columns['subunit_list'].create()
    pre_meta.tables['organisms'].columns['org_id_ncbi'].create()
