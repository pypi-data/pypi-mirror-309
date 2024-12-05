import os
from bs4 import BeautifulSoup


class AyehYab():

    def standard_text(self, text):
        text = (text.replace('\n', ' ')
                .replace('  ', ' ')
                .replace('ً', '')
                .replace('ٌ', '')
                .replace('ٍ', '')
                .replace('َ', '')
                .replace('ُ', '')
                .replace('ِ', '')
                .replace('ّ', '')
                .replace('ْ', '')
                .replace('ة', 'ه')
                .replace('ك', 'ک')
                .replace('ي', 'ی')
                .replace('ی', 'ی')
                .replace('ى', 'ی')
                .replace('ئ', 'ی')
                .replace('إ', 'ا')
                .replace('أ', 'ا')
                .replace('آ', 'ا')
                .replace('ء', 'ا')
                .replace('ؤ', 'و')
                .replace('.', '')
                .replace('؟', '')
                .replace('،', '')
                .replace('؛', '')
                .replace('-', '')
                .replace('_', '')
                .replace('(', '')
                .replace(')', '')
                .replace('{', '')
                .replace('}', '')
                .replace(']', '')
                .replace('[', '')
                .replace(']', '')
                .replace('[', '')
                .replace('»', '')
                .replace('«', '')
                .replace(':', '')
                .replace('"', '')
                .replace("'", '')
                .replace('\\', '')
                .replace('/', '')
                .replace('<', '')
                .replace('>', '')
                .replace('1', '')
                .replace('2', '')
                .replace('3', '')
                .replace('4', '')
                .replace('5', '')
                .replace('6', '')
                .replace('7', '')
                .replace('8', '')
                .replace('9', '')
                .replace('0', '')
                .replace('‏', '')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                .replace('  ', ' ')
                )
        text = text.strip()
        return text

    def ayeh_find(self,
                  text,
                  quran_url=None,
                  ayeh_class=None,
                  paragraph_mark=None,
                  tag=None,
                  min_word=None,
                  min_len_pure_text=None,
                  flag_identifying=None
                  ):
        if not quran_url: quran_url = 'https://data.belquran.com/fa-IR/Quran/s/'
        if not ayeh_class: ayeh_class = 'ayeh'
        if not paragraph_mark: paragraph_mark = '</br>'
        if not tag: tag = 'a'
        if not min_word: min_word = 3
        if not min_len_pure_text: min_len_pure_text = 10
        if not flag_identifying: flag_identifying = 1

        '''
        :param text: متن ورودی
        :param quran_url: شماره سوره و شماره آیه به این لینک اضافه شده و لینک روی آیه را ایجاد میکنند
                        این لینک باید به صورت زیر کار کند:
                        url/شماره سوره/شماره آیه
        :param ayeh_class: کلاسی که به تگ آیه سوار میشود
        :param paragraph_mark: از آنجا که ورودی به صورت لیستی از متنهاست این تگ چیزی است که مابین متنها در پاراگرافهای مختلف قرار میگیرد مانند
                                '</br>' یا '<p></p>' یا '<hr>' یا ''
        :param tag: تگی که متن آیه در آن قرار میگیرد باید به صورت تکست بدون علامت بزرگتر و کوچکتر باشد مانند
                    'p'  یا  'a'  یا  'span'  یا  'ayeh'  یا  'quran'
        :param min_word: حداقل تعداد کلمه ای که در جستجوی قرآنی شرکت میکند-اگر از 2 کمتر بود 2 در نظر گرفته میشود
        :param min_len_pure_text: حداقل تعداد حرف قسمت متن برای آیه یابی که اگر از 10 کمتر بود 10 در نظر گرفته میشود
        :param flag_identifying: در این کد اگر برای یک تکه متن چند آیه قرآن ناپیوسته پیشنهاد شود
                                یعنی آن تکه در قسمتهای مختلف قرآن موجود است
                                فلذا ابتدا با کل آدرس آیاتی که در کل متن ورودی هستند تطبیق داده میشود
                                اگر یکی از آدرس های اختصاص یافته به آن تکه متن یا +1 یا -1 آن در آدرسهای آن پاراگراف بود آن آدرس برگزیده میشود
                                در غیر این صورت اگر این فلگ صفر بود هیچ آدرسی برای آن تکه متن برگزیده نمیشود و صرفا تگ آیه به آن میخورد
                                و اگر این تگ یک بود اولین آدرس از بین آدرسهای اختصاص داده شده برگزیده میشود
        ***************************************************************************************************
        :return: خروجی به صورت یک دیکشنری است با سه کلید و مقدار
                html_output:
                    کلید اول متن به صورت html است که همان متن ورودی است و لیکن آیات آن با مقادیر مناسب تگ گذاری شده است
                    بر روی هر آیه title قرار داده شده به علاوه یک تگ مخصوص و همچنین لینک و همچنین یک attr برای تعیین شماره آیات
                    شماره آیات(ayehid) یک رشته از اعداد(شماره آیه) است. ممکن است یک عدد یا چند عدد که با , جدا شده اند در آن باشد
                list_output:
                    کلید دوم اطلاعات آیات پیدا شده در پاراگرافهاست که به صورت یک لیست از لیستهاست که درون هر کدام یک یا چند دیکشنری است
                    هر لیست داخلی متناظر با یک پاراگراف است
                    مقادیر دیکشنری عبارتند از:
                        ayehid: به صورت یک رشته که یک عدد و یا چند عدد که با ، جدا شده اند داشته باشد
                                البته اگر شماره آیه پیدا نشد این لیست تهی خواهد بود
                        ayeh_text: متن تکه ای از متن که به عنوان آیه تشخیص داده شده است
                        index_start_end: ایندکس ابتدایی و انتهایی تکه متنی که به عنوان آیه تشخیص داده شده است
                                        به صورت یک تاپل با دو عدد شروع و پایان
                        ayeh_adress_text: (این متن بر روی title میتواند سوار شود)آدرس متنی تکه متنی که به عنوان آیه شناسایی شده است
                        link_ayeh: لینکی که میتواند بر آن تکه متن سوار شود
                list_ayat:
                    در این کلید کل آیات به کار رفته در متن ورودی به صورت لیستی از اعداد ارائه میشود
        '''
        # به جای ' از &#39; یا &apos; استفاده کنید.
        # به جای " از &#34; یا &quot; استفاده کنید.
        quran_url = quran_url
        ayeh_class = ayeh_class
        paragraph_mark = paragraph_mark
        tag = tag
        min_word = min_word
        min_len_pure_text = min_len_pure_text
        if min_word < 2: min_word = 2
        if min_len_pure_text < 10: min_len_pure_text = 10

        current_dir = os.path.dirname(__file__)

        ayeh_ids = list(range(1, 6237))

        ayat_file = open(os.path.join(current_dir, "packages", "ayat.txt"), 'r', encoding='utf-8')
        ayat_list = ayat_file.readlines()
        ayat_list_text = '@'.join(ayat_list)
        ayat_list_text = ayat_list_text.replace('\n', '')
        ayat_list_text = self.standard_text(ayat_list_text)
        ayat_list = ayat_list_text.split('@')

        surehname_ayehnumber_file = open(os.path.join(current_dir, "packages", "surehname_ayehnumber.txt"), 'r',
                                         encoding='utf-8')
        surehname_ayehnumber_list = surehname_ayehnumber_file.readlines()
        surehname_ayehnumber_list = list(map(lambda x: x.replace("\n", ""), surehname_ayehnumber_list))

        surehnumber_ayehnumber_file = open(os.path.join(current_dir, "packages", "surehnumber_ayehnumber.txt"), 'r',
                                           encoding='utf-8')
        surehnumber_ayehnumber_list = surehnumber_ayehnumber_file.readlines()
        surehnumber_ayehnumber_list = list(map(lambda x: x.replace("\n", ""), surehnumber_ayehnumber_list))

        adress_ayeh_dict = dict(zip(ayeh_ids, surehname_ayehnumber_list))
        ayeh_link_dict = dict(zip(ayeh_ids, surehnumber_ayehnumber_list))

        ayeh_id = 0
        ayat_text = ''
        ayat_text_dict = {}  # حاوی ایندکس کاراکتر در رشته  ayat_text به عنوان کلید و ayehid به عنوان مقدار
        index_counter = 0
        # لیست قرآن را تبدیل به یک رشته میکند
        # ضمنا در یک دیکشنری به ازای هر index ، شماره آیه متناظرش را قرار میدهد(index کلید و ayehid مقدار است)
        for ayeh in ayat_list:
            ayat_text += ayeh + ' '
            ayeh_id += 1
            len_ayeh = len(ayeh) + 1
            for index in range(0, len_ayeh + 1):
                ayat_text_dict[index_counter + index] = ayeh_id
            index_counter += len_ayeh

        output = []
        rows = text
        if type(rows) == str:
            rows = [rows]
        if type(rows) != list: return ''
        rows_len = len(rows)
        for row in rows:
            row.replace('\n', '')
            if not row:
                output.append([])
                continue
            # لیستی از ایندکس های فاصله در متن ایجاد میکند ، 0 و ایندکس آخرین کاراکتر نیز در این لیست اضافه میشود
            # دلیل این کار این است که مرو در متن بر اساس فاصله ها باشد و نه بر اساس کاراکتر(کلمه مهم است و نه حروف)
            list_index = [0]
            for index in range(len(row)):
                if row[index] == ' ':
                    list_index.append(index)
            list_index.append(len(row))

            out = []
            start = 0
            start_index = 0
            end = len(list_index) - 1
            end_index = list_index[end]
            '''
            مرور در متن ورودی به این شکل است که از ابتدا تا انتهای متن در متن قرآن جستجو میشود
            اگر پیدا نشد یک space از انتها کم میشود و دوباره جستجو، اگر پیدا نشد دوباره و دوباره تا اینکه انتها به ابتدا میچسبد
            و یا اینکه یکی دو تا فاصله هنوز مانده باشد
            در این حالت انتها به انتهای متن ورودی میچسبد و ابتدا یکی بیشتر میشود و دوباره جستجو و اگر پیدا نشد یکی از انتها کم میشود
            تا اینکه ابتدا به انتها میچسبد و یا اینکه یکی دوتا هنوز به انتها مانده باشد که از حلقه خارج میشود
            (در هر جا ایندکس شروه یا پایان تغییر میکند و متن جدیدی از متن اصلی انتخاب میشود عملیات استانداردسازی انجام میشود)
            در هر کجا که پیدا شد ایندکس ابتدا و انتها متن در دیکشنری متن قرآن بررسی شده و ayehid آن که ممکن است یک یا چند آیه متوالی باشد استخراج میشود
            به همراه ایندکس در متن اصلی بدون استانداردسازی 
             البته اگر آیه پیدا شد از آنجاییکه ممکن است در جاهای مختلف قرآن آمده باشد، دوباره از آنجای قرآن به بعد دوباره جستجو میشود
            '''

            while start_index < end_index - 2:
                start_index = list_index[start]
                end_index = list_index[end]
                text = row[start_index:end_index]
                pure_text = self.standard_text(text)
                ayeh_ids = []
                if (pure_text.count(' ') >= min_word - 1
                        and len(pure_text) >= min_len_pure_text
                        and pure_text in ayat_text):
                    i = 0
                    while True:
                        index0 = ayat_text.find(pure_text, i)
                        if index0 == -1:
                            break
                        index1 = index0 + len(pure_text) - 1
                        i = index1
                        ayehid0 = ayat_text_dict[index0]
                        ayehid1 = ayat_text_dict[index1]
                        ayeh_ids.append(",".join(map(str, range(ayehid0, ayehid1 + 1))))

                    out.append({'ayehid': ayeh_ids,
                                'ayeh_text': row[start_index:end_index],
                                'index_start_end': (start_index, end_index),
                                'ayeh_adress_text': '',
                                'link_ayeh': '',
                                })
                    start += pure_text.count(' ') + 1
                    end = len(list_index) - 1
                else:
                    if end < 1: break
                    end -= 1
                    if end <= start + 1:
                        end = len(list_index) - 1
                        start += 1
            output.append(out)

        # ******************************** تصحیح ayehid ***************************
        '''
        از آنجا که ممکن است متن سلکت شده در چند جای قرآن پیدا شود و چند آدرس بگیرد
        متغیر ayehid یک لیست خواهد بود که یک یا چند آدرس را داراست
        اگر تکه متنی دارای بیش از یک آدرس بود به کمک لیست کل آیات کل متن ورودی یکی از آنها انتخاب میشود
        بدین صورت که اگر هر کدام از آدرسها و یا +1 و یا -1 آن در لیست کل آیات پیدا شد آن احتمال برگزیده میشود
        و اگر نشد بسته به انتخاب کاربر یا مورد اول لیست احتمالات برگزیده میشود و یا اینکه تهی برمیگردد
        '''
        list_ayat = []
        # تهیه لیست کل آدرس آیات کل متن ورودی
        for sublist in output:
            for dictionary in sublist:
                if 'ayehid' in dictionary:
                    temp = dictionary['ayehid']
                    for item in temp:
                        if ',' in item:
                            item = item.split(',')
                            for i in item:
                                list_ayat.append(int(i))
                        else:
                            list_ayat.append(int(item))
        # تصحیح آدرس آیات احتمال با توجه به لیست کل
        for sublist in output:
            for dictionary in sublist:
                if 'ayehid' in dictionary:
                    flag = False
                    temp = dictionary['ayehid']
                    if len(temp) == 1:
                        dictionary['ayehid'] = temp[0]
                        continue
                    for i in temp:
                        if ',' not in i:
                            if list_ayat.count(int(i)) > 1 or list_ayat.count(int(i) - 1) > 0 or list_ayat.count(
                                    int(i) + 1) > 0:
                                dictionary['ayehid'] = i
                                flag = True
                                break
                        else:
                            for j in i.split(','):
                                if list_ayat.count(int(j)) > 1 or list_ayat.count(int(j) - 1) > 0 or list_ayat.count(
                                        int(j) + 1) > 0:
                                    dictionary['ayehid'] = i
                                    flag = True
                                    break
                    if flag == False:
                        if flag_identifying:  # اگر کاربر انتخاب کرده که در صورت نبود آدرس مشابه، احتمال اول برگردد
                            dictionary['ayehid'] = temp[0]
                        else:  # یا خالی برگردد
                            dictionary['ayehid'] = ''

                            # *****************   ayeh_adress_text  مقدار دهی  ********************
        '''
        بر اساس مقدار ayehid تصحیح شده آدرس آیه به صورت متنی نیز بدست میآید که میتواند در title متن استفاده شود
        اگر آدرس آیه یکی بود آدرس متنی همان آیه خواهد بود
        و اگر آدرس به صورت آیات پیوسته بود آدرس متنی آیه اول و آخر با فاصله - ارائه میشوند
        '''
        list_ayat_output = []
        for sublist in output:
            for dictionary in sublist:
                if 'ayehid' in dictionary:
                    ids = dictionary['ayehid']
                    list_ayat_output.append(ids)
                if 'ayeh_adress_text' in dictionary:
                    ayeh_adress_text = ''
                    if ',' in ids:
                        ids_temp = ids.split(',')
                        ayeh_adress_temp0 = adress_ayeh_dict.get(int(ids_temp[0]))
                        ayeh_adress_temp1 = adress_ayeh_dict.get(int(ids_temp[-1]))
                        if ayeh_adress_temp0 and ayeh_adress_temp1:
                            ayeh_adress_text = ayeh_adress_temp0 + '-' + ayeh_adress_temp1
                    else:
                        if ids:
                            ayeh_adress_text = adress_ayeh_dict.get(int(ids))
                    dictionary['ayeh_adress_text'] = ayeh_adress_text

                # *****************   link_ayeh مقدار دهی  *********************
                '''
                بر اساس مقدار ayehid تصحیح شده لینک مناسب برای متن قران ساخته میشود
                چه آدرس آیه یکی باشد و یا چند آیه پیوسته باشد آدرس اول ملاک خواهد بود
                ایت آدرس به لینک ورودی کاربر و یا پیش فرض افزوده میشود و یک url را میسازد
                '''
                link_ayeh = ''
                if 'link_ayeh' in dictionary:
                    if ',' in ids:
                        ids = ids.split(',')[0]
                    if ids:
                        link_ayeh = quran_url + ayeh_link_dict.get(int(ids))
                    dictionary['link_ayeh'] = link_ayeh

        # ******************************** ساختhtml  ***************************
        '''
        بر اساس لیست output و مقادیر آن متن ورودی به صورت  html  در میاید
        به ترتیب از پاراگراف اول الی آخر
        ولی در هر پاراگراف از آیات آخر شروع میشود و در ایندکس های مشخص شده tag,link,class,title,attr قرار میگیرد
        '''
        html_output = []
        for index in range(rows_len):
            row = rows[index]
            output_items = output[index]
            if not output_items: continue
            for item in output_items[::-1]:
                start_index, end_index = item['index_start_end']
                ayehids = item["ayehid"]
                ayeh_adress_text = item["ayeh_adress_text"]
                link_ayeh = item["link_ayeh"]
                start_tag = f"<{tag} href='{link_ayeh}' class='{ayeh_class}' ayeh_id='{str(ayehids)}' title='{ayeh_adress_text}'>"
                end_tag = f'</{tag}>'
                row = row[:start_index] + start_tag + row[start_index:end_index] + end_tag + row[end_index:]

            html_output.append(row)
        html_output = f'{paragraph_mark}'.join(html_output)

        if list_ayat_output:
            list_ayat_output = ','.join(list_ayat_output)
            list_ayat_output = list_ayat_output.split(',')
            list_ayat_output = [int(item) for item in list_ayat_output if item]
            list_ayat_output = sorted(list(set(list_ayat_output)))

        return {
            'html_output': html_output,
            'list_output': output,
            'list_ayat': list_ayat_output
        }

    def clear_additions(self, html_text, tag=None, class_name=None):
        '''
        این تابع بدین منظور تهیه شده تا تمامی تگهایی که تابع آیه یاب به یک متن زده را حذف کند
        :param html_text: متن ورودی که به صورت یک رشته باید باشد(لزومی بر پاراگراف کردن نیست و یک متن بلند نیز در اینجا قابل بارگذاری است)
        :param tag:  تگی که باید حذف شود(به صورت پیش فرض تگ پیش فرض تابع آیه یاب را ملاک قرار میدهد)
        :param class_name: فقط آن تگهایی پاک میشوند که این کلاس را دارا باشند(به صورت پیش فرض همان کلاس تابع آیه یاب ملاک قرار گرفته است)
        :return: خروجی یک رشته خالی شده از کلیه ی تگها و اضافات تابع آیه یاب است
        '''
        if not tag: tag = 'a'
        if not class_name: class_name = 'ayeh'

        output = []
        for text in html_text:
            soup = BeautifulSoup(text, "html.parser")
            for tag in soup.find_all(name=tag, class_=class_name):
                tag.unwrap()  # حذف فقط تگ مربوطه و متعلقات آن
                # فقط متنهای داخل تگ a باقی مانده و مابقی چیزهایی که درون تگ a است حذف میشود حتی اگر تگهای دیگری در ان باز و بسته شده باشند
                # tag.replace_with(tag.get_text())
            output.append(str(soup))
        return output
