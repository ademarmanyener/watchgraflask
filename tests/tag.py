# -*- encoding: utf-8 -*-

def getTemplate(get_str):
  get_str = get_str.lower()
  ret_list = []
  ret_list.append('{} 1080p'.format(get_str))
  ret_list.append('{} türkçe hd'.format(get_str))
  ret_list.append('{} full izle'.format(get_str))
  ret_list.append('{} izle'.format(get_str))
  ret_list.append('{} türkçe dublaj'.format(get_str))
  ret_list.append('{} türkçe altyazı'.format(get_str))
  return ret_list

def main():
  print(str(getTemplate('Batman')))

main()