import json
import xml.etree.ElementTree as xmlTree


def get_statistic(items, get_description):
    stat_dict = dict()
    for news in items:
        words = list(filter(lambda x: len(x) > 6 and not isinstance(x, int), get_description(news).split()))
        for word in words:
            if word.lower() not in stat_dict.keys():
                stat_dict[word.lower()] = 1
            else:
                stat_dict[word.lower()] += 1

    sorted_stat = sorted(stat_dict, reverse=True, key=stat_dict.get)
    return sorted_stat[:10]


def get_json_stat(input_file):
    with open(input_file, encoding='utf8') as fp:
        json_data = json.load(fp)
        items = json_data['rss']['channel']['items']
        return get_statistic(items, lambda x: x['description'])


def get_xml_stat(input_file):
    xml_data = xmlTree.parse(input_file)
    channel = xml_data.find('channel')
    items = channel.findall('item')
    return get_statistic(items, lambda x: x.find('description').text)


if __name__ == '__main__':
    print('Топ 10 самых часто встречающихся в новостях слов длиннее 6 символов.')
    print(f'\tВ файле формата JSON: {get_json_stat("newsafr.json")}')
    print(f'\tВ файле формата XML: {get_xml_stat("newsafr.xml")}')
