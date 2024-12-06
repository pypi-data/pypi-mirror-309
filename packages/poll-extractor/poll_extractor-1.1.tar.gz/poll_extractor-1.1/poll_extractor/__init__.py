class Poll_extractor():
    def __init__(self, data):
        self.init_data = data
        self.data = [self.init_data]
        self.results = []
        self.plots = []
    
    def __f_i(self, _q):
        _q_i = int()
        _q_g = ''
        if len(self.data) == 0:
            raise ValueError('data is empty')
        quiz = self.data[0][0]
        found = False
        for j in range(len(quiz)):
            if _q == quiz[j][0]:
                _q_i = j
                found = True
                break
            elif _q in quiz[j][0]:
                _q_g = quiz[j][0]
                
        if not found:
            _error_text = f'Cannot find such a question: {_q}.'
            if _q_g != '':
                _error_text += f' Do you mean \'{_q_g}\'?'
            raise KeyError(_error_text)
        return _q_i
    
    def order(self, columns:tuple):
        for _r in self.results:
            _x_coords = columns
            _y_coords = []
            for _c in columns:
                if _c not in _r:
                    _y = 0
                    print(f'Beware: not found {_c}')
                else:
                    _y = _r[_c]
                _y_coords.append(_y)
            _plot = (_x_coords, _y_coords, sum(_y_coords))
            self.plots.append(_plot)
        return self
    
    def count(self, question:str):
        _q_i = self.__f_i(question)
        for _d in self.data:
            result = {}
            for _q in _d:
                if _q[_q_i][1] not in result:
                    result[_q[_q_i][1]] = 0
                result[_q[_q_i][1]] += 1
            self.results.append(result)
        return self
    
    def split(self, question:str, separate_answers:tuple):
        results = []
        _q_i = self.__f_i(question)
        for _d in self.data:
            for _as_list in separate_answers:
                result = []
                for quiz in _d:
                    if quiz[_q_i][1] in _as_list:
                        result.append(quiz)
                results.append(result)
        self.data = results
        return self
    
    def raw(self):
        return self.data
    
    def filter(self, question:str, answers:tuple):
        return self.split(question, (answers,))
    
    def group(self, init_columns:tuple, result_columns:tuple):
        if len(init_columns) != len(result_columns):
            raise ValueError(f'columns have not matching sizes')
        plots = []
        for _plot in self.plots:
            _x_coords = result_columns
            _y_coords = []
            for init_group in init_columns:
                _y = 0
                for sub_group in init_group:
                    _i = _plot[0].index(sub_group)
                    _y += _plot[1][_i]
                _y_coords.append(_y)
            plots.append((_x_coords, _y_coords, _plot[2]))
        self.plots = plots
        return self
        
    def norm(self, ndigits=0):
        to_round = ndigits != 0
        for i, v in enumerate(self.plots):
            for j in range(len(self.plots[i][1])):
                self.plots[i][1][j] /= self.plots[i][2]
                if to_round:
                    self.plots[i][1][j] = round(self.plots[i][1][j], ndigits=ndigits)
        return self
            
    def finish(self):
        result = []
        for plot in self.plots:
            result.append((plot[0], plot[1]))
        
        self.data = [self.init_data]
        self.results = []
        self.plots = []
        return result