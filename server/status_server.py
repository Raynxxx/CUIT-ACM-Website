from __init__ import *
import sys
from util import function

class DataTablesServer():
    def __init__(self, request, oj_name, headers):
        self.request = request
        self.oj_name = oj_name
        self.headers = headers
        self.result = {}
        self.start = 0
        self.length_of_need = 0
        self.order_args = ''
        self.order_dir = ''

    def filter_data(self):
        filter_args = ["user_name","run_id","pro_id","lang","run_time","memory","submit_time"]
        module_name = sys.modules['dao.dbSUBMIT']
        class_name = 'Submit'
        submit_table = getattr(module_name, class_name)
        query = submit_table.query
        if self.oj_name != 'all':
            query = query.filter(submit_table.oj_name==self.oj_name)
        if self.request['columns[0][search][value]'] != '':
            query = query.filter(submit_table.user_name.like('%'+self.request['columns[0][search][value]']+'%'))
        if self.request['columns[3][search][value]'] != '':
            query = query.filter(submit_table.pro_id.like('%'+self.request['columns[3][search][value]']+'%'))
        if self.request['columns[5][search][value]'] != '':
            query = query.filter(submit_table.lang.like('%'+self.request['columns[5][search][value]']))
        if self.request['columns[2][search][value]'] != '':
            query = query.filter(submit_table.oj_name == self.request['columns[2][search][value]'])
        return query


    def parse_data(self):
        # get the request form args
        self.start = int(self.request['start'])
        self.length_of_need = int(self.request['length'])
        self.order_args = self.request['columns[' + str(self.request['order[0][column]']) + '][data]']
        self.order_dir = self.request['order[0][dir]']
        # get the Database class to get
        module_name = sys.modules['dao.dbSUBMIT']
        class_name = 'Submit'
        submit_table = getattr(module_name, class_name)
        order = getattr(submit_table, self.order_args)
        # make the response data
        filtered_data = self.filter_data()
        self.result['draw'] = self.request['draw']
        self.result['recordsTotal'] = str(filtered_data.count())
        self.result['recordsFiltered'] = self.result['recordsTotal']
        # order the data
        if self.order_dir == 'desc':
            tables = filtered_data.order_by(order.desc()).offset(self.start).limit(self.length_of_need).all()
        else:
            tables = filtered_data.order_by(order.asc()).offset(self.start).limit(self.length_of_need).all()
        return tables

    def run_query(self):
        tables = self.parse_data()
        data = []
        from config import OJ_MAP
        for row in tables:
            status = {
                'id': row.id,
                'oj_name': OJ_MAP[row.oj_name],
                'pro_id': function.submit_problem_page(row.oj_name,row.pro_id),
                'run_id':"<a href='/viewcode/{url}'>".format(url=row.oj_name+'/'+row.run_id) + row.run_id+"</a>",
                'submit_time': row.submit_time,
                'run_time': str(row.run_time) + ' MS',
                'memory': str(row.memory) + ' KB',
                'result': "<span style='color:{color}'>{res}</span>".format(res=row.result,
                                                                            color=function.submit_result_color(row.result)),
                'lang': row.lang,
                'user_name': row.user_name
            }
            if row.oj_name == 'cf':
                status['run_id'] = "<a href='{url}' target='_black'>".format(url=row.code) + row.run_id+"</a>",
            if status['memory'] == '-1 KB':
                status['memory'] = ''
            if status['run_time'] == '-1 MS':
                status['run_time'] = ''
            data.append(status)
        self.result['data'] = data
        return self.result
