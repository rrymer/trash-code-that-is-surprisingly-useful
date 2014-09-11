# -*- coding: utf-8 -*-
"""
Created on Sat May 24 17:03:13 2014

@author: pczrr
"""

def select_seq(table,refIDs,groupby,**queries):
    connection = connect_to_mysqdb('localhost', 'FamilyCpolymerases', 'sequser')
    cursor = connection.cursor()
    results_dict={}
    for ID in refIDs:
        logger.info("sql query for reference sequence:\n{}".format("select {}, {} from {} where {} = '{}'"
        .format(ID_field,seq_field,table,ID_field,refID)))
        cursor.execute("select {}, {} from {} where {} = '{}'".format(ID_field,seq_field,table,ID_field,refID))
        ref_seqs=dict(cursor.fetchall())
        results_dict[ID]=ref_seqs
        logger.info('executing argument queries: {}'.format(str(queries)))
    for nm,q in queries:
        logger.info("sql query for sample sequences:\n{}".format("select {}, {} from {} {} {}"
        .format(ID_field,seq_field,table,q,groupby)))
        cursor.execute("select {}, {} from {} {} {}".format(ID_field,seq_field,table,q,groupby))
        results=dict(cursor.fetchall())
        results_dict[nm]=results
    connection.close()
    return ref_seqs,results_dict

def sql_constructor(table,qdict):
    sql = "select * from ({})"
    subsql="{}"
    subgrpsql="{}"
    grpsqls={}
    i=0
    for nm,rslts in qdict.iteritems():
        for ID,x in rslts.iteritems():
            qxsql = "select '{}', {} where {} = '{}'".format(nm.format(ID),s v eq_field,ID_field,ID)
            subsql = subsql.format(qxsql)
        subgrpsql=subgrpsql.format(subsql)d
    grpsqls[grps[i]]=subsql
    for qID,sql in grpsqls.iteritems():
        sql = sql.format("{} = '{}'".format(ID_field,refIDs[table]))
        main_logger.info('final sql query for data set {}:{}'.format(nm,sql))
    return fasta_export(grpsqls)

def fasta_export (grp,seq_dict):
    with open(workingdir+'/Data/{}'.format(grp + '_seqs.txt'),'a') as outfile:
        for nm,rslts in seq_dict.iteritems():
            for ID,seq in rslts:
                outfile.write('>{}\n{}'.format(nm.format(ID),seq))
    expsql="{} into outfile '/tmp/{}.fasta' fields terminated by '\n' lines starting by '>'"
    for nm,sql in sql_dict:
        logger.info("sql statement for {}:{}".format(nm,expsql.format(sql,nm)))
        cursor.execute(expsql.format(sql,nm))
    connection.close()
