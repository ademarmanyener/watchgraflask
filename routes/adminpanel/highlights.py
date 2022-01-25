# -*- encoding: utf-8 -*-
from includes import *

@app.route('/adminpanel/highlights')
@app.route('/yoneticipaneli/onecikarilanlar')
def adminpanel_highlights():
  if not check_admin(): return redirect(url_for('home'))

  RET_URL = url_for('adminpanel_highlights') + '?page=1&sort=newest&list_count=10'

  ARG_PAGE = request.args.get('page', default=1, type=int)
  ARG_SORT = request.args.get('sort', default='newest', type=str)
  ARG_LIST_COUNT = request.args.get('list_count', default=10, type=int)
  DEF_OFFSET = (ARG_PAGE - 1) * ARG_LIST_COUNT

  # page validation begin
  if not ARG_PAGE >= 1: return redirect(RET_URL) 
  # page validation end

  # get query filters begin
  if ARG_SORT == 'newest': _db_sort = highlightContent.highlightDate.desc()
  elif ARG_SORT == 'oldest': _db_sort = highlightContent.highlightDate.asc()
  # get query filters end

  get_results = highlightContent.query.order_by(_db_sort).offset(DEF_OFFSET).limit(ARG_LIST_COUNT).all()
  DEF_PAGE_MAX = ceil(len(highlightContent.query.all()) / ARG_LIST_COUNT)

  # url args validation begin
  if not request.args.get('page') or not request.args.get('sort') or not request.args.get('list_count'): return redirect(RET_URL)
  # url args validation end 

  return render_template('adminpanel/highlights/list.html', title='Öne Çıkarılan İçerikler', list_results_info=get_results, \
                                        _ARG = {
                                          'page': ARG_PAGE, 'page_max': DEF_PAGE_MAX,
                                          'sort': ARG_SORT,
                                          'list_count': ARG_LIST_COUNT,
                                        })
