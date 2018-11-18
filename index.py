# Import
import codecs
import sys
with codecs.open('sms.txt', encoding='utf-8', errors='ignore') as file:
    smslist = [line.strip().replace('\x00', '').split('\t') for line in file.readlines()]

# Sanitize
smslistsanitized = []
for sms in smslist:
    if len(sms) >= 5:
        smslistsanitized.append({'corresponder': sms[0], 'date': sms[2], 'content': sms[4]})
    else:
        smslistsanitized[-1]['content'] += ''.join(sms)
smslist = smslistsanitized
print(len(smslist), 'SMS loaded')

# Compute

#Code pour compter les occurences d'un mot dans tous les SMS :
concerned = []
counter = 0
word = sys.argv[1]
print('word:', word)
for sms in smslist:
    tmp = sms['content'].lower().count(word.lower())
    if tmp > 0:
        counter += tmp
        concerned.append(sms)

#Code pour savoir quel contact répond le plus :
concerned2 = []
listenum = {}
counter2 = 0
num = sys.argv[1]
for sms in smslist:
    tmp2 = sms['corresponder']
    if tmp2 :
        counter2 += 1
        concerned2.append(sms['corresponder'])
        print('tmp2 ' + tmp2)
        if sms['corresponder'] not in listenum :
            listenum[sms['corresponder']] = 1
            continue
        else :
            listenum[sms['corresponder']] += 1

listenum2 = sorted(listenum.items(), key=lambda t: t[1], reverse=True)
for i in listenum:
    print ('Appel:' + i)
    print(listenum[i])

#Code pour savoir quel contact écrit le plus de caractères:
plusgrandpave = {}
num3 = sys.argv[1]
for sms in smslist:
    tmp3 = sms['corresponder']
    if tmp3 :
        plusgrandpave[sms['corresponder']] = len(sms['content'])
        continue

plusgrandpave = sorted(plusgrandpave.items(), key=lambda t: t[1], reverse=True)

print(plusgrandpave)
print('nombre de caractères : ' + str(plusgrandpave[0][1]) + ' pour le numéro : ' + str(plusgrandpave[0][0]))

# Code pour faire un graphe de fréquence de SMS :
days = {}
for sms in smslist:
    date = sms['date'].split(' ')[0]
    if date not in days:
        days[date] = 0
    days[date] += 1
    # print(days[date])

# Export

# Code pour faire un graphe :
import matplotlib.pyplot as plt
plt.plot(days.values())
plt.ylabel('number of sms')
#plt.show() # <-- pour afficher un preview
plt.savefig('graph.png')

# graphe nombre sms par num :
import numpy as np
import matplotlib.pyplot as plt2
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

n_groups = len(listenum2)

means_men = []
for i in listenum2:
    means_men.append(i)
print(means_men)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 1
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, [elt[1] for elt in means_men], bar_width,
                alpha=opacity, color='b',
                error_kw=error_config,
                label='Nombre de sms')

ax.set_xlabel('Nums')
ax.set_ylabel('Nombre de sms')
ax.set_title('Nombre de sms par numéro')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels = []
for i in listenum2:
    means_men.append(i)
ax.legend()

fig.tight_layout()
plt2.savefig('graph2.png')

# Code pour faire un HTML :
with open('output.html', 'w', encoding='utf-8') as file:
    file.write('<!DOCTYPE html><html><head><meta charset="utf-8" /><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.2/css/bootstrap.min.css" integrity="sha384-Smlep5jCw/wG7hdkwQ/Z5nLIefveQRIY9nfy6xoR1uRYBtpZgI6339F5dgvm/e9B" crossorigin="anonymous"></head><body><div class="container">')
    file.write('<h1> Le mot "' + word + '" a été trouvé ' + str(counter) + ' fois</h1>')

    file.write('<h2> Quelques valeurs : </h2>')
    file.write('<table class="table table-dark"><thead><tr><th scope="col">Valeurs</th><th scope="col">Contenu</th></tr></thead><tbody>')

    file.write('<tr>')
    file.write('<th scope="row">Contact le plus actif : </th><td>' + listenum2[0][0] + ' : (' +  str(listenum2[0][1]) + ' messages)</td>')
    file.write('</tr>')

    file.write('<tr>')
    file.write('<th scope="row">Plus grand message : </th><td>' + plusgrandpave[0][0] + ' : (' +  str(plusgrandpave[0][1]) + ' caractères)</td>')
    file.write('</tr>')

    file.write('</tbody></table>')
    file.write('<h2> Courbes de valeurs : </h2>')
    file.write('<div class="row"><div class="col-6"><img class="img-fluid" src="graph.png"></div>')
    file.write('<div class="col-6"><img class="img-fluid" src="graph2.png"></div></div>')

    file.write('<table class="table table-dark"><thead><tr><th scope="col">Num</th><th scope="col">Message</th></tr></thead><tbody>')
    for sms in concerned:
        file.write('<tr>')
        file.write('<th scope="row">' + sms['corresponder']+ '</th>' + '<td>' + sms['content'] + '</td>')
        file.write('</tr>')
    file.write('</tbody></table></div></body></html>')
