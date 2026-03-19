import streamlit as st
import json
import time
import random
import os
from datetime import datetime

# ── Page Config ──
st.set_page_config(page_title="EPSO Sprachlogik Trainer", page_icon="🧠", layout="centered")

# ── Constants ──
TIME_LIMIT = 105  # 1:45 per question

# ── 30 Verified Questions ──
VERIFIED = [
# EPSO Official (10)
{"id":"epso-1","source":"EPSO Official","text":"Ein gängiges Blutdruckmittel könnte Menschen, die ein traumatisches Erlebnis hatten, helfen, sich von ihren quälenden Erinnerungen zu befreien. Ein Drittel der Personen, die ein belastendes Erlebnis hatten, leiden unter posttraumatischen Belastungsstörungen. Schon ein Geräusch oder ein Geruch kann die Erinnerung an dieses Erlebnis wieder wachrufen. Patienten mit dieser Störung erhalten eine Beratung. Da diese jedoch nicht immer wirksam ist, suchen Forscher nach alternativen Therapien. Studien haben gezeigt, dass Ratten, die konditioniert waren, auf bestimmte Ereignisse im Labor mit Angst zu reagieren, nach Verabreichung des Medikaments ihre Angst verloren. Dies deutet darauf hin, dass das Medikament zur Behandlung posttraumatischer Belastungsstörungen beitragen könnte.","question_type":"correct","options":[{"letter":"A","statement":"Posttraumatische Belastungsstörungen hängen mit zu hohem Blutdruck zusammen."},{"letter":"B","statement":"Es ist unwahrscheinlich, dass Patienten, die unter posttraumatischen Belastungsstörungen leiden, sich von alleine erholen."},{"letter":"C","statement":"Geräusche oder Gerüche können Erinnerungen an belastende Erlebnisse wachrufen."},{"letter":"D","statement":"Bei der Behandlung posttraumatischer Belastungsstörungen ist die Beratung in der Regel unwirksam."}],"correct":"C","explanation":"C korrekt: Der Text sagt explizit 'Schon ein Geräusch oder ein Geruch kann die Erinnerung wachrufen.' A: Kein Zusammenhang PTBS/Blutdruck. B: Nichts über Selbstheilung (NICHT_IM_TEXT). D: 'nicht immer wirksam' ≠ 'in der Regel unwirksam' (GEWICHTUNG).","trap_type":"GEWICHTUNG"},
{"id":"epso-2","source":"EPSO Official","text":"Die Methode der kleinsten Quadrate ist eine statistische Methode zur Berechnung einer Geraden oder einer Kurve, die das Verhältnis zwischen zwei Messgrößen am besten repräsentiert. Werden die Messungen als Punkte auf einen Graphen übertragen und liegen sie nahe an derselben Linie, so kann zur Bestimmung der Modellkurve die Methode der kleinsten Quadrate angewandt werden. Die Parameter dieser Kurve werden numerisch bestimmt, indem die Summe der quadratischen Abweichungen der Kurve von den beobachteten Punkten minimiert wird. Man spricht von Regression oder, wenn die Linie eine Gerade und keine Kurve ist, von linearer Regression.","question_type":"correct","options":[{"letter":"A","statement":"Die Methode der kleinsten Quadrate wird in der Praxis kaum angewandt."},{"letter":"B","statement":"Die lineare Regression berechnet den Abstand von Datenpunkten zu einer Horizontalen."},{"letter":"C","statement":"Die Methode der kleinsten Quadrate ermöglicht das Anlegen einer Modellkurve, die die Datenpunkte für zwei Messgrößen am besten repräsentiert."},{"letter":"D","statement":"Die Methode der kleinsten Quadrate funktioniert am besten bei Kurven."}],"correct":"C","explanation":"C gibt den Kern korrekt wieder. A: Nicht im Text. B: Abweichung von der Modellkurve, nicht einer Horizontalen. D: Kein Vorteil bei Kurven erwähnt.","trap_type":"NICHT_IM_TEXT"},
{"id":"epso-3","source":"EPSO Official","text":"Haiku sind eine Form der japanischen Dichtung, die keine Reime kennt. Haiku bestehen aus 17 Silben, die entweder eine einzige Zeile oder drei Zeilen mit jeweils fünf, sieben und fünf Silben füllen. Das Gedicht enthält stets einen Hinweis auf die Jahreszeit, die den Rahmen bildet. Haiku-Dichter drücken möglichst viel mit möglichst wenigen Worten aus. Diese Form wurde durch den Dichter Basho im 17. Jahrhundert bekannt gemacht. In Japan sind Haiku auch heute noch die beliebteste Form der Dichtung.","question_type":"correct","options":[{"letter":"A","statement":"Haiku nutzen subtile Reime, um die Bedeutung des Gedichts zum Ausdruck zu bringen."},{"letter":"B","statement":"In längeren Haiku-Gedichten wird die Struktur von fünf, sieben und fünf Silben in mehrzeiligen Versen wiederholt."},{"letter":"C","statement":"Haiku enthalten in der Regel drei Wörter mit fünf, sieben bzw. fünf Silben."},{"letter":"D","statement":"Haiku enthalten immer einen Hinweis auf die Jahreszeit, die den Rahmen bildet."}],"correct":"D","explanation":"D korrekt: 'stets' = 'immer'. A: Widerspricht direkt ('keine Reime'). B: Nicht im Text. C: Verwechselt Silben mit Wörtern (QUANTITAET).","trap_type":"QUANTITAET"},
{"id":"epso-4","source":"EPSO Official","text":"Lemuren sind eine Familie aus der Ordnung der Primaten. Man nimmt an, dass sie ursprünglich in Afrika verbreitet waren, heute sind sie jedoch nur noch auf Madagaskar und einigen umliegenden Inseln anzutreffen, einschließlich der Komoren (wohin sie wahrscheinlich von den Menschen gebracht wurden). Ihr Körpergewicht reicht vom 30 g schweren Zwerg-Mausmaki bis zum 10 kg schweren Indri. Früher gab es noch größere Arten, die aber seit der Ansiedlung der Menschen ausgestorben sind. Die kleineren Lemurenarten sind meist nachtaktiv und die größeren tagaktiv, es gibt aber auch Ausnahmen.","question_type":"correct","options":[{"letter":"A","statement":"Lemuren lebten schon auf Madagaskar, bevor die Insel von Menschen besiedelt wurde."},{"letter":"B","statement":"Lemuren kommen von Natur aus auf den Komoren vor."},{"letter":"C","statement":"Indris sind nur tagsüber aktiv."},{"letter":"D","statement":"Das Aussterben der größten Lemurenarten ist eine unmittelbare Folge der Ansiedlung der Menschen."}],"correct":"A","explanation":"A korrekt: Größere Arten starben 'seit der Ansiedlung der Menschen' aus → Lemuren waren vorher da. B: 'wahrscheinlich von Menschen gebracht'. C: 'es gibt Ausnahmen' widerspricht 'nur' (GENERALISIERUNG). D: Zeitlicher Zusammenhang ≠ unmittelbare Folge (KAUSALITAET).","trap_type":"KAUSALITAET"},
{"id":"epso-5","source":"EPSO Official","text":"Hauptziele des Programms Marco Polo sind die Verringerung der Überlastung der Straßen und die Verbesserung der Umweltfreundlichkeit des gesamten Verkehrssystems. Das Programm soll einen verkehrspolitischen Kurs unterstützen, der im Weißbuch der Kommission dargelegt wurde. Dort wird empfohlen, die Verkehrsträgeranteile im Güterverkehr bis 2010 wieder auf die Höhe von 1998 zurückzuführen. Die Aktionen sollen dazu beitragen, den Straßengüterverkehr auf den Kurzstreckenseeverkehr, die Schiene und die Binnenschifffahrt zu verlagern.","question_type":"correct","options":[{"letter":"A","statement":"Die Verlagerung des Straßengüterverkehrs soll sich positiv auf die Umwelt auswirken."},{"letter":"B","statement":"Das Programm wurde eingeführt, weil der internationale Straßengüterverkehr erheblich zugenommen hat."},{"letter":"C","statement":"Im Weißbuch stehen die Umweltauswirkungen im Vordergrund, nicht die Überlastung der Straßen."},{"letter":"D","statement":"Der Gütertransport auf Schiene und Binnenschifffahrt ist seit 1998 insgesamt zurückgegangen."}],"correct":"A","explanation":"A ableitbar: Umweltfreundlichkeit ist Hauptziel + Verlagerung ist Maßnahme. B: Nicht im Text (NICHT_IM_TEXT). C: Beide Ziele gleichwertig (GEWICHTUNG). D: Nicht ableitbar.","trap_type":"NICHT_IM_TEXT"},
{"id":"epso-6","source":"EPSO Official","text":"Die Herausbildung der auf Europa ausgerichteten Weltwirtschaft im 19. Jahrhundert war geprägt durch ein System von Nationalstaaten, die zueinander in Wettbewerb standen. Kein Staat war allein stark genug, um die anderen zu beherrschen. Im Gegensatz zu früheren Systemen wie dem Reich der Habsburger, in dem die Stabilität der Wirtschaft von der Stabilität des Reiches abhing, konnte in diesem neuen Weltsystem die Wirtschaft auch dann fortbestehen, wenn ein Staat zusammenbrach.","question_type":"correct","options":[{"letter":"A","statement":"Das Habsburgerreich brach aufgrund wirtschaftlicher Instabilität zusammen."},{"letter":"B","statement":"Durch den Wettbewerb wurde die Wirtschaft des neuen Weltsystems stabiler."},{"letter":"C","statement":"Die Weltwirtschaft war das Ergebnis des Handelns eines dominanten Staates."},{"letter":"D","statement":"Der Zusammenbruch eines Nationalstaats hätte die Weltwirtschaft erheblich geschwächt."}],"correct":"B","explanation":"B korrekt: Wettbewerb → Wirtschaft überlebt Zusammenbrüche = stabiler. A: Nicht im Text. C+D: Widersprechen direkt.","trap_type":"NICHT_IM_TEXT"},
{"id":"epso-7","source":"EPSO Official","text":"Die Antarktis ist der kälteste Kontinent. Ihre Eisdecke umfasst 90% des gesamten Gletschereises der Welt. Der Russe F.G. von Bellingshausen zählte zur Gruppe der Forscher, die nach eigenen Aussagen 1820 als erste den Kontinent erblickten. Anfang des 20. Jahrhunderts erforschten Expeditionen das Innere. Sieben Nationen erhoben Gebietsansprüche, obwohl sie nie dauerhaft besiedelten. 1958 errichteten zwölf Nationen Forschungsstationen.","question_type":"correct","options":[{"letter":"A","statement":"Der erste Mensch, der die Antarktis erblickte, war ein Russe."},{"letter":"B","statement":"Anfang des 20. Jahrhunderts erhoben sieben Länder Gebietsansprüche, 1958 stieg die Zahl auf zwölf."},{"letter":"C","statement":"In der Antarktis befindet sich mehr Gletschereis als auf allen anderen Kontinenten zusammen."},{"letter":"D","statement":"In der Antarktis gab es nie dauerhaft menschliche Bewohner."}],"correct":"C","explanation":"C korrekt: 90% = mehr als alle anderen (10%) zusammen. A: 'zur Gruppe' ≠ er war der Erste (GENERALISIERUNG). B: 12 errichteten Stationen, nicht Gebietsansprüche (QUANTITAET). D: Geht über den Text hinaus.","trap_type":"GENERALISIERUNG"},
{"id":"epso-8","source":"EPSO Official","text":"Gentests sind medizinische Verfahren, mit denen Veränderungen an Genen festgestellt werden können. Meistens dienen Gentests dazu, Erbkrankheiten zu erkennen. Durch Gentests kann die Wahrscheinlichkeit festgestellt werden, dass ein Mensch erkrankt oder eine Krankheit vererbt. Derzeit werden mehrere Hundert Gentests verwendet; weitere werden entwickelt. Die Entscheidung ist jedem selbst überlassen. Viele bezweifeln die Nützlichkeit, da sie glauben, dass nur tödliche Krankheiten nachgewiesen werden.","question_type":"correct","options":[{"letter":"A","statement":"Im Allgemeinen werden gesunde Menschen Gentests unterzogen."},{"letter":"B","statement":"Mit Gentests kann die Wahrscheinlichkeit festgestellt werden, dass jemand an einer bestimmten Krankheit erkrankt."},{"letter":"C","statement":"Gentests sind nicht sinnvoll, weil sie freiwillig sind."},{"letter":"D","statement":"Jährlich werden mehrere Hundert Gentests durchgeführt."}],"correct":"B","explanation":"B korrekt laut Text. A: Nicht im Text. C: Falsche Kausalität. D: 'verwendet' (als Verfahren) ≠ 'jährlich durchgeführt'.","trap_type":"KAUSALITAET"},
{"id":"epso-9","source":"EPSO Official","text":"Moldau ist eine Region im Nordosten Rumäniens. Bis 1859 war Moldau ein unabhängiger Staat. Heute bildet sie einen großen Teil des modernen rumänischen Staates. In der Geschichte gehörten Bessarabien und Bukowina zu Moldau. Ein Großteil Bessarabiens bildet heute die Republik Moldau, während der Rest Bessarabiens und der Norden Bukowinas zur Ukraine gehören.","question_type":"correct","options":[{"letter":"A","statement":"Das Gebiet der historischen Moldau ist heute auf mindestens drei Staaten verteilt."},{"letter":"B","statement":"Der Staat Moldau war bis 1859 Teil der Region Moldau."},{"letter":"C","statement":"Die Region Moldau erstreckt sich auf dasselbe Gebiet wie der Staat Moldau."},{"letter":"D","statement":"Bessarabien und Bukowina bilden heute die Republik Moldau bzw. die Ukraine."}],"correct":"A","explanation":"A korrekt: Rumänien + Republik Moldau + Ukraine = drei Staaten. B: Verdreht. C: Widerspricht. D: Nur ein 'Großteil', nicht ganz (QUANTITAET).","trap_type":"QUANTITAET"},
{"id":"epso-10","source":"EPSO Official","text":"Die Gambel-Eiche ist ein kleiner Baum, der gewöhnlich in 1700-2400 m Höhe wächst. Er ist im mittleren Südwesten der USA verbreitet. Gambel-Eichen gedeihen an Hängen mit dünnem, steinigem Erdboden, wo andere Pflanzen nur begrenzt wachsen. Sie können auch in fruchtbarerem Boden überleben, sind dort aber größerer Konkurrenz ausgesetzt. Selbst schwer verbrannt, kann sich die Gambel-Eiche aus ihren Wurzeln regenerieren.","question_type":"correct","options":[{"letter":"A","statement":"Gambel-Eichen gedeihen an Hängen, an denen keine anderen Pflanzen überleben können."},{"letter":"B","statement":"Gambel-Eichen sind in den ganzen Vereinigten Staaten verbreitet."},{"letter":"C","statement":"Gambel-Eichen gedeihen besser mit weniger Konkurrenz durch andere Pflanzen."},{"letter":"D","statement":"Die Gambel-Eiche kann nicht durch Feuer zerstört werden."}],"correct":"C","explanation":"C korrekt: Weniger Konkurrenz = besseres Gedeihen. A: 'nur begrenzt' ≠ 'keine' (GENERALISIERUNG). B: Nur 'mittlerer Südwesten' (GENERALISIERUNG). D: 'kann sich regenerieren' ≠ 'kann nicht zerstört werden' (GENERALISIERUNG).","trap_type":"GENERALISIERUNG"},
# Deutsche Übungsfragen (20)
{"id":"de-1","source":"Übungsfragen DE","text":"Höhenkrankheit ist eine durch längeren Aufenthalt in großen Höhen verursachte Erkrankung mit psychischen und physischen Symptomen. Sie kann auch andere höhenbedingte Erkrankungen auslösen wie Höhenlungenödeme, die ohne Behandlung tödlich verlaufen können. Höhenkrankheit kommt in der Regel in Höhen von über 2500 m vor. Die Schwere der Symptome ist von Mensch zu Mensch unterschiedlich. Bei manchen zeigen sich bereits Anzeichen in 1500 m Höhe. Anhaltende Kopfschmerzen sind ein erstes Symptom. Weitere Symptome sind Müdigkeit, Schwindel und Übelkeit.","question_type":"correct","options":[{"letter":"A","statement":"Mit der Höhe nimmt auch die Schwere der Symptome der Höhenkrankheit zu."},{"letter":"B","statement":"Höhenkrankheit kann zum Tode führen, wenn sie andere höhenbedingte Erkrankungen auslöst."},{"letter":"C","statement":"Zu den Symptomen eines Höhenlungenödems zählen Kopfschmerzen und Übelkeit."},{"letter":"D","statement":"Höhenkrankheit tritt selten unter 1500 m auf."}],"correct":"B","explanation":"B korrekt: Höhenlungenödeme können 'ohne Behandlung tödlich verlaufen'. A: Schwere ist 'von Mensch zu Mensch unterschiedlich', nicht höhenabhängig (NICHT_IM_TEXT). C: Kopfschmerzen sind Symptome der Höhenkrankheit, nicht des Lungenödems (KAUSALITAET). D: 'In der Regel über 2500 m' ≠ 'selten unter 1500 m' (QUANTITAET).","trap_type":"KAUSALITAET"},
{"id":"de-2","source":"Übungsfragen DE","text":"Um einen Anruf von einem Bürotelefon aus zu tätigen, nimmt man den Hörer ab und wählt die Nummer. Man muss keine 9 wählen, um eine externe Nummer anzurufen. Wenn man einen Anruf in die Warteschleife legen möchte, drückt man die Rückruf-Taste. Man kann den Anrufer dann nicht mehr hören, und der Anrufer kann einen selbst ebenfalls nicht mehr hören. Wenn man den Anrufer hören möchte, dieser einen jedoch nicht hören soll, drückt man die Stummschalttaste. Um weiterzuleiten, hält man den Anruf in der Warteschleife, gibt die Durchwahlnummer ein und legt auf. Wenn ein anderes Telefon klingelt, kann man den Anruf annehmen, indem man *30 wählt.","question_type":"correct","options":[{"letter":"A","statement":"Wenn man nicht möchte, dass der Anrufer einen hört, kann man entweder die Stummschalttaste oder die Rückruftaste drücken."},{"letter":"B","statement":"Man kann einen Anruf weiterleiten, indem man *30 wählt."},{"letter":"C","statement":"Man muss nur dann die 9 wählen, wenn man eine Person im selben Büro anruft."},{"letter":"D","statement":"Mit der Rückruftaste kann man einen anderen Anruf annehmen."}],"correct":"A","explanation":"A korrekt: Beide Tasten bewirken, dass der Anrufer einen nicht hört. B: *30 ist zum Annehmen, nicht Weiterleiten (KAUSALITAET). C: Man muss die 9 gar nicht wählen. D: *30, nicht die Rückruftaste (KAUSALITAET).","trap_type":"KAUSALITAET"},
{"id":"de-3","source":"Übungsfragen DE","text":"Fragen Sie sich einmal, wo Ihr Ich sitzt, und Sie werden antworten: 'Hinter meinen Augen, zwischen meinen Ohren'. Vor zwanzig Jahren dachte David Hawley Sanford darüber nach, wie man uns ein Gefühl geben könnte, wir befänden uns außerhalb unseres Körpers. So ersann er die Augen-Videos. 'Sie projizieren das Bild direkt auf die Netzhaut und messen jede Bewegung des Augapfels. Die Kameras folgen den schnellsten Augenbewegungen. Zwischen dem Sehen mit Augen-Videos und dem mit eigenen Augen gibt es keinen Unterschied'.","question_type":"correct","options":[{"letter":"A","statement":"Mit Hilfe von Augen-Videos kann man den eigenen Körper verlassen."},{"letter":"B","statement":"Mit Hilfe von Augen-Videos kann man den eigenen Standort ändern."},{"letter":"C","statement":"Das Sehen mit Hilfe eines Augen-Videos hat genau denselben Effekt wie das Sehen mit bloßem Auge."},{"letter":"D","statement":"Augen-Videos sind Kameras in Form eines Auges."}],"correct":"C","explanation":"C korrekt: 'Zwischen dem Sehen mit Augen-Videos und dem mit eigenen Augen gibt es keinen Unterschied.' A: Es geht um ein 'Gefühl', nicht Tatsache (GENERALISIERUNG). B: Standort soll nicht geändert werden. D: Über die Form sagt der Text nichts (NICHT_IM_TEXT).","trap_type":"NICHT_IM_TEXT"},
{"id":"de-4","source":"Übungsfragen DE","text":"Wenn man sich für ein Haustier entscheidet, denken viele nicht daran, wie lange die Erziehung eines Hundes dauert. Fachleute sagen, jeder Hund muss fortwährend erzogen werden. Besonders gilt dies für größere Hunde, die von Natur aus aggressiver sind. Hunde sind gesellige Rudeltiere. Viele lassen ihren Hund den größten Teil des Tages allein. Einige binden ihre Hunde draußen an, was aggressives Verhalten fördern kann. Es führt zu 'Ungenügender Sozialisation'. Ein Hundeausbilder rät: 'Achten Sie darauf, dass Ihr Hund täglich mit vielen Leuten zusammenkommt'.","question_type":"correct","options":[{"letter":"A","statement":"Wer einen aggressiveren Hund will, muss bedenken, dass die Erziehung sehr zeitaufwendig wird."},{"letter":"B","statement":"Ein Hund einer guten Rasse hat ein geringeres Risiko für aggressives Verhalten."},{"letter":"C","statement":"Hunde werden aggressiv, wenn ihre Besitzer sie lange alleine lassen."},{"letter":"D","statement":"Einen Hund anzubinden, erhöht das Risiko aggressiven Verhaltens."}],"correct":"D","explanation":"D korrekt: 'Anbinden kann aggressives Verhalten fördern.' A: 'Fortwährend' ≠ 'zeitaufwendig'. B: Über 'gute Rassen' sagt der Text nichts (NICHT_IM_TEXT). C: Alleinlassen → ungenügende Sozialisation, nicht direkt Aggression (KAUSALITAET).","trap_type":"KAUSALITAET"},
{"id":"de-5","source":"Übungsfragen DE","text":"Eine 'Rahmenerzählung' basiert auf einer fortlaufenden Geschichte, in der nicht viel passiert. Die Personen sind z.B. Pilger, die gemeinsam reisen (Chaucers Canterbury-Erzählungen) oder eine Gruppe in einem Haus (Boccaccios Decamerone oder Sades 120 Tage von Sodom). In Zabaras Werk begeben sich der Erzähler und Enan in eine Stadt, die als ideal dargestellt wird, sich aber als Enttäuschung erweist. Das eigentliche Geschehen findet in den Nebenhandlungen statt, die sich zu einem kohärenten Ganzen zusammenfügen.","question_type":"correct","options":[{"letter":"A","statement":"Eine 'Rahmenerzählung' ist eine fortlaufende Geschichte, in der sehr viel passiert."},{"letter":"B","statement":"In Chaucers Canterbury-Erzählungen sind die Personen in einem Haus zu Gast und erzählen sich Geschichten."},{"letter":"C","statement":"Boccaccios Decamerone ist ein Beispiel für eine Rahmenerzählung, in der die Personen einander Geschichten erzählen."},{"letter":"D","statement":"Wenn Menschen gemeinsam reisen und sich Geschichten erzählen, ist das eine Rahmenerzählung."}],"correct":"C","explanation":"C korrekt: Decamerone = Beispiel Rahmenerzählung mit Geschichten. A: Gegenteil ('nicht viel passiert'). B: Canterbury = Pilger die reisen, nicht Haus (KAUSALITAET). D: Zu einfache Definition.","trap_type":"KAUSALITAET"},
{"id":"de-6","source":"Übungsfragen DE","text":"Ein Achtel aller Vogelarten wird wahrscheinlich nicht bis zum Ende des Jahrhunderts überleben. Sie zählen zu den 1186 Arten, die laut BirdLife vom Aussterben bedroht sind. Obwohl das UN-Übereinkommen über biologische Vielfalt (1992) Besorgnis äußert, hat sich die Lage nicht verbessert. In zehn Jahren mussten zwei weitere Arten (Waldvögel aus Hawaii) auf die Liste der ausgestorbenen Arten gesetzt werden, und ca. 100 Arten wurden als 'stark gefährdet' eingestuft. 182 Arten haben nur 50% Überlebenschance für die nächsten zehn Jahre.","question_type":"correct","options":[{"letter":"A","statement":"Etwa 50% der gefährdeten Vogelarten werden wahrscheinlich nicht bis ins nächste Jahrhundert überleben."},{"letter":"B","statement":"Das UN-Übereinkommen über die biologische Vielfalt konnte keinen hinreichenden Schutz der Vögel gewährleisten."},{"letter":"C","statement":"Immer mehr hawaiianische Vogelarten sterben aus."},{"letter":"D","statement":"Das Überleben von 182 Vogelarten ist bereits in Gefahr."}],"correct":"B","explanation":"B korrekt: Übereinkommen → 'Lage hat sich nicht verbessert' = unzureichend. A: 'Ein Achtel', nicht 50% (QUANTITAET). C: 'Immer' ist absolut – nur 2 Arten erwähnt (GENERALISIERUNG). D: 50% Chance ≠ 'bereits in Gefahr' (GEWICHTUNG).","trap_type":"GENERALISIERUNG"},
{"id":"de-7","source":"Übungsfragen DE","text":"Um Adipositas-Vorbeugung zu ermitteln, wurde ein europaweites Fachleute-Netz aufgebaut. Die Kommission hat Rechtsvorschriften über nährwertbezogene Aussagen vorgeschlagen. Mehr als die Hälfte der EU-Erwachsenen sind übergewichtig. Bis zu 7% der Gesundheitshaushalte werden für Adipositas-Krankheiten ausgegeben. Gesundheitsexperten sind sich einig über die Ursachen: passive Bevölkerung mit sitzender Lebensweise, die Nahrungsmittel mit immer höherem Energiegehalt zu sich nimmt. Strittig ist jedoch, was dagegen unternommen werden kann.","question_type":"correct","options":[{"letter":"A","statement":"Bewegungsmangel gilt als einer der wesentlichen Faktoren für Übergewicht."},{"letter":"B","statement":"Die im Handel erhältlichen Lebensmittel sind gesundheitsschädlich."},{"letter":"C","statement":"Die Bevölkerung hat eine sitzende Lebensweise, weil ihre Ernährung immer mehr Energie enthält."},{"letter":"D","statement":"Nährwertbezogene Aussagen führen dazu, dass sich Verbraucher gesünder ernähren."}],"correct":"A","explanation":"A korrekt: 'Passive Bevölkerung mit sitzender Lebensweise' = Bewegungsmangel als Ursache. B: 'Gesundheitsschädlich' steht nicht im Text (NICHT_IM_TEXT). C: Beide sind Ursachen, nicht Ursache-Wirkung (KAUSALITAET). D: Aussagen sollen informieren, nicht automatisch zu gesünderer Ernährung führen (KAUSALITAET).","trap_type":"KAUSALITAET"},
{"id":"de-8","source":"Übungsfragen DE","text":"Die EU-Kommission hat gegen die beiden größten französischen Brauereigruppen Geldbußen verhängt wegen einer Vereinbarung, mit der sie der Kostenexplosion bei Übernahmen von Großhändlern Einhalt gebieten und ein Gleichgewicht zwischen ihren Vertriebsnetzen herbeiführen wollten. Sie vereinbarten einen befristeten Übernahmestopp und eine ausgewogene Aufteilung der Biermengen. Die Vereinbarung diente der Kontrolle der Investitionen und kam einer Marktaufteilung gleich. Die Geldbuße berücksichtigt, dass die Vereinbarung nie angewandt wurde und folgenlos blieb.","question_type":"correct","options":[{"letter":"A","statement":"Die Kommission hat die Bierhersteller aufgefordert, Übernahmen einzustellen."},{"letter":"B","statement":"Die Vereinbarung sollte die Kostensteigerung beim Erwerb von Großhändlern stoppen."},{"letter":"C","statement":"Die Geldbuße wurde verhängt, weil die Investitionstätigkeit beschränkt wurde."},{"letter":"D","statement":"Durch die Vereinbarung hätte ein Erzeuger den Markt beherrschen können."}],"correct":"B","explanation":"B korrekt: 'Der Kostenexplosion Einhalt gebieten' = Kostensteigerung stoppen. A: Die Unternehmen vereinbarten den Stopp selbst (KAUSALITAET). C: Geldbuße wegen Marktaufteilung, nicht Investitionsbeschränkung. D: Gleichgewicht, nicht Dominanz.","trap_type":"KAUSALITAET"},
{"id":"de-9","source":"Übungsfragen DE","text":"Die EU-Kommission unterstützt seit vielen Jahren Forschungsarbeiten zur Gehörlosigkeit. 50% aller Hörbehinderungen sind genetisch bedingt. Die Ermittlung der genetischen Faktoren ist von zentraler Bedeutung, um die Ursachen zu erkennen. Heute ist es möglich, diese Faktoren zu ermitteln. Das Wissen über den Hörvorgang wurde vertieft. Neue Therapiemöglichkeiten werden erschlossen. In Tierversuchen gelang es, Hörschwächen zu simulieren.","question_type":"correct","options":[{"letter":"A","statement":"Genetische Faktoren werden von einer Generation zur nächsten weitergegeben."},{"letter":"B","statement":"Genetische Faktoren ermöglichen es, Gehörlosigkeit rückgängig zu machen."},{"letter":"C","statement":"Die Ermittlung genetischer Faktoren ermöglicht es, die Ursache der Gehörlosigkeit zu erkennen."},{"letter":"D","statement":"Die Ermittlung genetischer Faktoren ermöglicht die Diagnose der Gehörlosigkeit."}],"correct":"C","explanation":"C korrekt: Text sagt 'Ursachen zu erkennen'. A: Über Weitergabe nichts im Text (NICHT_IM_TEXT). B: 'Rückgängig machen' geht weit über den Text hinaus (GENERALISIERUNG). D: Ursache erkennen ≠ Gehörlosigkeit diagnostizieren (QUANTITAET).","trap_type":"NICHT_IM_TEXT"},
{"id":"de-10","source":"Übungsfragen DE","text":"Die Farbe des Universums ist ein ganz helles Grün. Diese Frage war nie Gegenstand eines Forschungsvorhabens, aber als zwei amerikanische Astronomen sahen, dass die Antwort anhand vorliegender Daten ermittelt werden konnte, waren sie nicht mehr zu bremsen. Diese Farbe ist der Durchschnittswert anderer Durchschnittswerte. Bei den Forschungsarbeiten ging es darum, Lichtemissionen von Sternen in verschiedenen Galaxien und Epochen zu vergleichen. Die Wissenschaftler hoffen festzustellen, ob früher mehr neue Sterne entstanden als jetzt. Die Antwort lautet offenbar: 'ja'.","question_type":"correct","options":[{"letter":"A","statement":"Zwei Astronomen waren neugierig auf die Farbe des Universums."},{"letter":"B","statement":"Die Farbe des Universums ist äußerst mittelmäßig."},{"letter":"C","statement":"Zwei Wissenschaftler forschten über die Farbe des Universums."},{"letter":"D","statement":"Heutzutage entstehen nur wenige neue Sterne."}],"correct":"A","explanation":"A korrekt: Sie 'waren nicht mehr zu bremsen' = Neugier. B: 'Durchschnittswerte' ≠ 'mittelmäßig' (QUANTITAET). C: Die Forschung galt Lichtemissionen, nicht der Farbe (KAUSALITAET). D: 'Weniger als früher' ≠ 'nur wenige' (GENERALISIERUNG).","trap_type":"QUANTITAET"},
{"id":"de-11","source":"Übungsfragen DE","text":"Eine Gruppe von Architekten beabsichtigt, Brachland in einen tropischen Regenwald zu verwandeln, in dem Wärme durch Zersetzung von Abfällen erzeugt wird. Dieses 150-Mio-Euro-Projekt soll die Regenerierung eines Ödland-Gebiets ermöglichen und könnte eine Touristenattraktion werden. Geplant sind der höchste Wasserfall des Landes und Europas größter Komposthaufen. Der Wald soll von fünfzig Meter hohen Mauern aus Schutt mit Kompostierungsröhren umgeben sein. In diese werden Grünabfall, verdorbene Lebensmittel und Textilien eingebracht.","question_type":"correct","options":[{"letter":"A","statement":"Der Regenwald dient in erster Linie dem Naturschutz."},{"letter":"B","statement":"Den Architekten wurde die Genehmigung erteilt."},{"letter":"C","statement":"Energie soll aus Grünabfall, Lebensmitteln und Kunststoffabfall erzeugt werden."},{"letter":"D","statement":"Recyclingmaterial soll zur Schaffung und Erhaltung des Regenwalds dienen."}],"correct":"D","explanation":"D korrekt: Abfälle und Schutt = Recyclingmaterial. A: 'Könnte Touristenattraktion werden' – nicht primär Naturschutz (GEWICHTUNG). B: 'Beabsichtigt' ≠ Genehmigung (GENERALISIERUNG). C: Kunststoff wird nicht erwähnt – Textilien ja (NICHT_IM_TEXT).","trap_type":"NICHT_IM_TEXT"},
{"id":"de-12","source":"Übungsfragen DE","text":"In der EU sind besondere Produktbezeichnungen, die mit einem Produktionsgebiet oder einer Produktionsmethode zusammenhängen, gesetzlich geschützt. Geschützte Bezeichnungen werden durch ein Qualitätssiegel kenntlich gemacht. Vorteile: Verbraucher bekommen authentische Erzeugnisse garantierter Herkunft; geografische Angaben übermitteln Werbebotschaften; der Handel kann über Merkmale und Herkunft informieren. Verbraucher und Handel sind zunehmend am geografischen Ursprung interessiert.","question_type":"correct","options":[{"letter":"A","statement":"Das Qualitätssiegel gewährleistet, dass das Erzeugnis einer bestimmten Marke zugehörig ist."},{"letter":"B","statement":"Das Qualitätssiegel dient vor allem Werbezwecken."},{"letter":"C","statement":"Das Qualitätssiegel gewährleistet, dass das Erzeugnis keine Nachahmung ist."},{"letter":"D","statement":"Die Informationen werden vor allem vom Verbraucher verlangt."}],"correct":"C","explanation":"C korrekt: 'Authentisches Erzeugnis garantierter Herkunft' = keine Nachahmung. A: Nicht Marke, sondern Gebiet/Methode. B: 'Vor allem' ist unzulässig – es gibt verschiedene Vorteile (GEWICHTUNG). D: 'Verbraucher und Handel' gleichermaßen (GEWICHTUNG).","trap_type":"GEWICHTUNG"},
{"id":"de-13","source":"Übungsfragen DE","text":"Wir brauchen Metrologen. Am Ende des 18. Jahrhunderts herrschte bei Maßen und Gewichten Chaos, was den Handel erheblich belastete. Vor zweihundert Jahren gab es in den Niederlanden 55 'Normen' für die Maßeinheit 'Fuß'. Mit der Einführung des metrischen Systems wurde vereinheitlicht. Die europäischen Maße basieren auf dem SI-System, das Urmaße für Meter, Sekunde, Kilogramm, Grad Kelvin, Candela und Mol beinhaltet.","question_type":"correct","options":[{"letter":"A","statement":"Das SI-System, zu dem auch das Mol zählt, wurde eingeführt, um in der chaotischen Welt der Maße Ordnung zu schaffen."},{"letter":"B","statement":"Vor zweihundert Jahren gab es in den Niederlanden 55 verschiedene Längenmaße."},{"letter":"C","statement":"Das SI-System bildete die Grundlage für das metrische System."},{"letter":"D","statement":"Weil der Handel litt, wurde im 18. Jahrhundert das metrische System eingeführt."}],"correct":"A","explanation":"A korrekt: SI-System enthält Mol und dient der Vereinheitlichung. B: 55 'Normen' für Fuß, nicht 55 verschiedene Längenmaße (QUANTITAET). C: Umgekehrte Reihenfolge. D: Zeitpunkt der Einführung nicht im Text (CHRONOLOGIE).","trap_type":"QUANTITAET"},
{"id":"de-14","source":"Übungsfragen DE","text":"Seit 1950 ist die Nahrungsmittelproduktion erheblich gestiegen. In entwickelten Gebieten betrug der Anstieg 1950-1975 115%, in unterentwickelten lag er noch höher. Dieses Wachstum führte aber nicht zu gleicher Versorgungssteigerung. In entwickelten Gebieten stieg die Versorgung wegen geringerem Bevölkerungswachstum. In unterentwickelten war das Bevölkerungswachstum stärker. Die Pro-Kopf-Versorgung nahm dort zwar zu, lag aber unter dem selbstgesteckten Ziel.","question_type":"correct","options":[{"letter":"A","statement":"Die unterentwickelten Gebiete erzeugten 1950-1975 mehr Nahrungsmittel als die entwickelten."},{"letter":"B","statement":"Die Pro-Kopf-Versorgung blieb in unterentwickelten Gebieten relativ unverändert."},{"letter":"C","statement":"Die unterentwickelten Gebiete hatten 1975 eine ausreichende Versorgung."},{"letter":"D","statement":"Die Pro-Kopf-Produktion war in entwickelten Gebieten 1975 nicht schlechter als 1950."}],"correct":"D","explanation":"D korrekt: Produktion +115% + geringes Bevölkerungswachstum = Pro-Kopf mindestens gleich. A: Höherer Prozentsatz ≠ höhere absolute Menge (QUANTITAET). B: 'Nahm zu' widerspricht 'unverändert'. C: 'Unter dem Ziel' ≠ ausreichend (GEWICHTUNG).","trap_type":"QUANTITAET"},
{"id":"de-15","source":"Übungsfragen DE","text":"Rechte an geistigem Eigentum sind komplex und für akademische Forschungskreise strategisch bedeutsam. In einer Welt zunehmender Patentierung sehen sie darin ein Mittel, Ergebnisse zu schützen und Einnahmen zu erzielen, um unzureichende Fördermittel auszugleichen. Zwei Fragen werden debattiert: Birgt die 'Allround-Patentierung' die Gefahr, die Verbreitung von Kenntnissen zu hemmen? Und: Die Kosten der Verfahren überfordern bisweilen öffentliche Forschungseinrichtungen.","question_type":"correct","options":[{"letter":"A","statement":"Öffentliche Fördermittel müssen vollständig durch Patenteinnahmen ersetzt werden."},{"letter":"B","statement":"Rechte an geistigem Eigentum sind mit dem Ziel der öffentlichen Forschung völlig vereinbar."},{"letter":"C","statement":"Die Verfahren für geistiges Eigentum sind in Europa zu komplex."},{"letter":"D","statement":"Keine der obigen Aussagen trifft zu."}],"correct":"D","explanation":"D korrekt. A: 'Ausgleichen' ≠ 'vollständig ersetzen' (GENERALISIERUNG). B: Zielkonflikt wird beschrieben. C: 'Komplex' beschreibt die Problematik, nicht die Verfahren; 'Europa' nicht erwähnt (NICHT_IM_TEXT).","trap_type":"GENERALISIERUNG"},
{"id":"de-16","source":"Übungsfragen DE","text":"Laut Pythagoras kann man Musik von perfekter Schönheit komponieren, die alle Kulturen und die Zeit transzendiert, wenn man die richtigen mathematischen Verhältnisse wahrt. Moderne Musikwissenschaftler haben dieser Vorstellung den Garaus gemacht, aber nichtsdestotrotz lässt sich etwas Sinnvolles über den universellen Wert der Musik sagen: Die Musik hat in der Entwicklung der Menschheit eine äußerst wichtige Rolle gespielt.","question_type":"correct","options":[{"letter":"A","statement":"Pythagoras war überzeugt, dass perfekte Schönheit in der Musik nur durch bestimmte mathematische Verhältnisse erzielt werden könne."},{"letter":"B","statement":"Musikwissenschaftler halten es für sinnvoll, sich universelle Musik anzuhören."},{"letter":"C","statement":"Alle Kulturen haben Musik, deren Schönheit alle Grenzen überschreitet."},{"letter":"D","statement":"Das Verhältnis von Mathematikern zur Musik ist kompliziert."}],"correct":"A","explanation":"A korrekt: Text sagt 'laut Pythagoras... wenn man die richtigen mathematischen Verhältnisse wahrt'. B: 'Universelle Musik' ≠ 'universeller Wert' (QUANTITAET). C: Pythagoras' Idee wurde widerlegt. D: Nicht im Text (NICHT_IM_TEXT).","trap_type":"NICHT_IM_TEXT"},
{"id":"de-17","source":"Übungsfragen DE","text":"Genauso wie ein Wolf nicht ohne sein Rudel überleben kann, so braucht auch der Hund einen Herrn. Anhänglichkeit ist ein strategisches Verhalten, das die Überlebenschancen vergrößern soll. Manchmal ist diese Anhänglichkeit mit etwas gekoppelt, was wir für Treue halten. Manchmal auch mit Tricks und Schläue. Ein kluger Hund wird seine Zuneigungsbekundungen einsetzen, um Nahrung zu ergattern!","question_type":"correct","options":[{"letter":"A","statement":"Da ein Hund ein Rudel braucht, kann er ohne einen Herrn nicht überleben."},{"letter":"B","statement":"Wenn ein Hund Zuneigung zeigt, ist dies Teil einer Überlebensstrategie."},{"letter":"C","statement":"Haustiere benutzen Tricks, um Nahrung zu ergattern."},{"letter":"D","statement":"Da Hunde ähnlich aussehen wie Wölfe, ist auch ihr Verhalten ähnlich."}],"correct":"B","explanation":"B korrekt: 'Anhänglichkeit ist ein strategisches Verhalten, das die Überlebenschancen vergrößern soll.' A: 'Braucht' ≠ 'kann nicht überleben' (GENERALISIERUNG). C: Text spricht nur von Hunden, nicht Haustieren allgemein (GENERALISIERUNG). D: Über äußere Ähnlichkeit nichts im Text (NICHT_IM_TEXT).","trap_type":"GENERALISIERUNG"},
{"id":"de-18","source":"Übungsfragen DE","text":"Hinweise auf Erasmus sind in Rotterdam überall zu finden. Da ist die Erasmusbrücke über die Maas, ein elegantes Wunder der Architektur, das bei starkem Wind ins Wanken gerät. Und die Erasmus-Universität, die heutzutage weniger philosophisch gesinnte Wirtschaftswissenschaftler und Juristen hervorbringt, aber eine Stätte der Gelehrsamkeit ist. Außerdem gibt es ein Erasmus-Umzugsunternehmen, eine Erasmus-Keksfabrik, einen Erasmus-Kindergarten und vieles mehr.","question_type":"correct","options":[{"letter":"A","statement":"Nach Erasmus sind u.a. eine Keksfabrik und eine Grundschule benannt."},{"letter":"B","statement":"Die Erasmusbrücke ist infolge starken Windes ins Wanken geraten und eingestürzt."},{"letter":"C","statement":"Philosophie ist nicht Teil des Lehrplans für Wirtschaftswissenschaftler."},{"letter":"D","statement":"Die nach Erasmus benannte Brücke ist von großer architektonischer Eleganz."}],"correct":"D","explanation":"D korrekt: 'Elegantes Wunder der Architektur'. A: Kindergarten, nicht Grundschule (NICHT_IM_TEXT). B: 'Gerät ins Wanken' ≠ 'eingestürzt' (GENERALISIERUNG). C: 'Philosophisch gesinnt' bezieht sich auf Gesinnung, nicht Lehrplan (KAUSALITAET).","trap_type":"NICHT_IM_TEXT"},
{"id":"de-19","source":"Übungsfragen DE","text":"Daten über gefährdete Vogelarten bilden die Grundlage für Schutzbemühungen, so Joke Winkelman. 'Der Rückgang ist bei 99 Prozent der Arten auf menschliches Handeln zurückzuführen. Natürlich haben auch Naturereignisse zu Artensterben geführt, wie der Ausbruch des Krakatoa 1883. Auch durch El Nino gab es für einige Arten auf den Galapagosinseln Probleme.'","question_type":"correct","options":[{"letter":"A","statement":"Wir können gefährdete Vogelarten schützen, indem wir viel über sie herausfinden."},{"letter":"B","statement":"Viele Vogelarten sterben infolge von Naturkatastrophen aus."},{"letter":"C","statement":"Vogelarten sterben sowohl infolge menschlichen Verhaltens als auch infolge von Naturkatastrophen aus."},{"letter":"D","statement":"Wegen El Nino sind mehrere Vogelarten ausgestorben."}],"correct":"C","explanation":"C korrekt: Beide Ursachen werden genannt (99% menschlich + Naturereignisse). A: Datensammlung ist Grundlage, nicht direkt Schutz (KAUSALITAET). B: 'Viele' ≠ 1% der Fälle (QUANTITAET). D: El Nino verursachte 'Probleme', nicht Aussterben (GENERALISIERUNG).","trap_type":"QUANTITAET"},
]

# ── Trap Labels & Tips ──
TRAP_LABELS = {
    "CHRONOLOGIE": "⏱ Zeitlicher Ablauf",
    "KAUSALITAET": "↔ Falsche Ursache-Wirkung",
    "QUANTITAET": "🔢 Falsche Mengen/Zahlen",
    "NICHT_IM_TEXT": "❌ Nicht im Text",
    "GEWICHTUNG": "⚖ Unzulässige Gewichtung",
    "GENERALISIERUNG": "🔍 Vom Besonderen aufs Allgemeine",
}

TRAP_TIPS = {
    "CHRONOLOGIE": "Prüfen Sie die zeitliche Reihenfolge: 'danach' ≠ 'davor', 'seit' ≠ 'vor'.",
    "KAUSALITAET": "Zusammen erwähnt ≠ Ursache-Wirkung. 'X bewirkt Y' muss explizit im Text stehen.",
    "QUANTITAET": "Achten Sie auf Zahlen: 'Ein Drittel' ≠ 'die Mehrheit'. Prozente genau prüfen.",
    "NICHT_IM_TEXT": "Nur der Text zählt! Egal wie plausibel – wenn es nicht drin steht, ist es falsch.",
    "GEWICHTUNG": "Vorsicht bei 'hauptsächlich', 'nur', 'vor allem'. Nennt der Text mehrere Aspekte gleichwertig?",
    "GENERALISIERUNG": "Text: 'Viele/Einige/Häufig' → Antwort: 'Alle/Jeder/Immer' = FALSCH.",
}

# ── AI Question Generation ──
def generate_ai_question(api_key, previous_topics=""):
    """Generate a question using Claude API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        system = """Du bist EPSO-Testentwickler für AD5-Sprachlogik (Deutsch). Generiere eine Aufgabe.

EPSO-REGELN:
- Text: ca. 130 Wörter, sachlich
- Frage: "Welche Antwort kann am besten aus dem Text abgeleitet werden?"
- 4 Optionen (A/B/C/D), genau EINE richtig
- Allgemeinwissen spielt KEINE Rolle

DIE 6 NICHT-ÜBEREINSTIMMUNGSTYPEN für falsche Optionen:
1. CHRONOLOGIE: Falscher zeitlicher Ablauf
2. KAUSALITAET: Falsche Ursache-Wirkung
3. QUANTITAET: Falsche Mengen/Zahlen
4. NICHT_IM_TEXT: Plausibel aber nicht im Text
5. GEWICHTUNG: "hauptsächlich/nur/vor allem" wo Text gleichwertig
6. GENERALISIERUNG: "Viele" → "Alle", "Einige" → "Jeder"

FORMAT (NUR JSON):
{"text":"...","question_type":"correct","options":[{"letter":"A","statement":"..."},{"letter":"B","statement":"..."},{"letter":"C","statement":"..."},{"letter":"D","statement":"..."}],"correct":"B","explanation":"...","trap_type":"KAUSALITAET"}"""

        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": f"Neue Aufgabe. Themen vermeiden: {previous_topics}. NUR JSON."}]
        )
        text = msg.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        q = json.loads(text)
        q["source"] = "KI-generiert"
        q["id"] = f"ai-{int(time.time())}"
        if "question_type" not in q:
            q["question_type"] = "correct"
        return q
    except Exception as e:
        st.error(f"KI-Fehler: {e}")
        return None

# ── Session State Init ──
if "stats" not in st.session_state:
    st.session_state.stats = {"total": 0, "correct": 0, "wrong": 0, "timeout": 0, "traps": {}, "best_streak": 0}
if "session" not in st.session_state:
    st.session_state.session = []
if "current_q" not in st.session_state:
    st.session_state.current_q = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "used_ids" not in st.session_state:
    st.session_state.used_ids = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "session_size" not in st.session_state:
    st.session_state.session_size = 10

# ── Styling ──
st.markdown("""
<style>
    .stApp { max-width: 700px; margin: 0 auto; }
    div[data-testid="stButton"] button {
        width: 100%;
        text-align: left;
        padding: 12px 16px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: white;
        font-size: 14px;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #2E75B6;
        background: #f0f4f8;
    }
    .correct-answer { background-color: #d4edda !important; border-color: #2D8B4E !important; }
    .wrong-answer { background-color: #f8d7da !important; border-color: #C0392B !important; }
</style>
""", unsafe_allow_html=True)

def get_next_question():
    """Get next question (verified first, then AI)"""
    available = [q for q in VERIFIED if q["id"] not in st.session_state.used_ids]

    if available and random.random() < 0.65:
        q = random.choice(available)
        st.session_state.used_ids.append(q["id"])
        return q

    # Try AI if API key is set
    api_key = st.session_state.get("api_key", "")
    if api_key:
        prev = ", ".join([q.get("text", "")[:25] for q in st.session_state.session[-3:]])
        return generate_ai_question(api_key, prev)

    # Fallback to verified (even if used before)
    if VERIFIED:
        q = random.choice(VERIFIED)
        return q
    return None

def show_home():
    st.markdown("### 🧠 Sprachlogisches Denken")
    st.caption("EPSO AD5 · Deutsch · 1:45/Frage · 30 verifizierte + KI-Fragen")

    # API Key (optional)
    with st.expander("⚙️ Anthropic API-Key (optional, für KI-generierte Fragen)"):
        api_key = st.text_input("API Key", type="password", key="api_key_input")
        if api_key:
            st.session_state.api_key = api_key
            st.success("API-Key gesetzt. KI-Fragen aktiviert.")
        else:
            st.info("Ohne API-Key nur die 30 verifizierten Fragen.")

    # Session size
    st.markdown("**Session-Größe:**")
    cols = st.columns(4)
    for i, n in enumerate([5, 10, 15, 20]):
        with cols[i]:
            if st.button(str(n), key=f"size_{n}",
                        type="primary" if st.session_state.session_size == n else "secondary"):
                st.session_state.session_size = n
                st.rerun()

    remaining = len([q for q in VERIFIED if q["id"] not in st.session_state.used_ids])
    st.caption(f"{remaining} verifizierte Fragen übrig · {st.session_state.session_size} Fragen pro Session")

    # Start button
    if st.button("▶️ Session starten", type="primary", use_container_width=True):
        st.session_state.session = []
        st.session_state.screen = "question"
        q = get_next_question()
        if q:
            st.session_state.current_q = q
            st.session_state.answered = False
            st.session_state.selected = None
            st.session_state.start_time = time.time()
        st.rerun()

    # Stats
    s = st.session_state.stats
    if s["total"] > 0:
        st.markdown("---")
        st.markdown("**📊 Gesamtstatistik**")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Gesamt", s["total"])
        c2.metric("✓", s["correct"])
        c3.metric("✗", s["wrong"])
        c4.metric("⏱", s["timeout"])
        c5.metric("🔥 Beste", s["best_streak"])

        pct = round((s["correct"] / s["total"]) * 100)
        st.progress(pct / 100, text=f"{pct}% Trefferquote")

        if s["traps"]:
            st.markdown("**Häufigste Fehlertypen:**")
            sorted_traps = sorted(s["traps"].items(), key=lambda x: x[1], reverse=True)
            for trap, count in sorted_traps[:5]:
                label = TRAP_LABELS.get(trap, trap)
                tip = TRAP_TIPS.get(trap, "")
                st.markdown(f"- {label}: **{count}×** — _{tip}_")

def show_question():
    q = st.session_state.current_q
    if not q:
        st.session_state.screen = "home"
        st.rerun()
        return

    session = st.session_state.session
    size = st.session_state.session_size

    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f"**{len(session) + 1}** / {size}")
    with col2:
        elapsed = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
        remaining = max(0, TIME_LIMIT - elapsed)
        if not st.session_state.answered:
            mins = remaining // 60
            secs = remaining % 60
            color = "green" if remaining > 60 else ("orange" if remaining > 30 else "red")
            st.markdown(f"<h3 style='text-align:center;color:{color}'>{mins}:{secs:02d}</h3>", unsafe_allow_html=True)
    with col3:
        s = st.session_state.stats
        st.markdown(f"✓ {s['correct']} · ✗ {s['wrong'] + s['timeout']}")

    # Source badge
    if q.get("source") == "EPSO Official" or q.get("source") == "Übungsfragen DE":
        st.caption(f"✦ Verifizierte Frage · {q['source']}")
    else:
        st.caption("🤖 KI-generierte Frage")

    # Text
    st.markdown(f"""<div style="background:#f8f9fb;border-left:4px solid #2E75B6;padding:16px;border-radius:8px;margin-bottom:16px;line-height:1.8">{q['text']}</div>""", unsafe_allow_html=True)

    # Question
    is_incorrect = q.get("question_type") == "incorrect"
    if is_incorrect:
        st.markdown("⚠️ **Welche Aussage ist NICHT zutreffend?**")
    else:
        st.markdown("**Welche Antwort kann am besten aus dem Text abgeleitet werden?**")

    # Options
    for opt in q["options"]:
        letter = opt["letter"]
        statement = opt["statement"]
        is_selected = st.session_state.selected == letter
        is_correct = letter == q["correct"]

        if st.session_state.answered:
            if is_correct:
                prefix = "✅"
            elif is_selected:
                prefix = "❌"
            else:
                prefix = "⬜"
            st.markdown(f"{prefix} **{letter})** {statement}")
        else:
            if st.button(f"{letter})  {statement}", key=f"opt_{letter}"):
                elapsed = int(time.time() - st.session_state.start_time)
                st.session_state.selected = letter
                st.session_state.answered = True
                ok = letter == q["correct"]

                # Update stats
                stats = st.session_state.stats
                stats["total"] += 1
                if ok:
                    stats["correct"] += 1
                    st.session_state.streak += 1
                    stats["best_streak"] = max(stats["best_streak"], st.session_state.streak)
                else:
                    stats["wrong"] += 1
                    st.session_state.streak = 0
                    trap = q.get("trap_type", "OTHER")
                    stats["traps"][trap] = stats["traps"].get(trap, 0) + 1

                st.session_state.session.append({
                    **q, "user": letter, "ok": ok, "time": min(elapsed, TIME_LIMIT)
                })
                st.rerun()

    # Check timeout
    if not st.session_state.answered:
        elapsed = int(time.time() - st.session_state.start_time)
        if elapsed >= TIME_LIMIT:
            st.session_state.answered = True
            st.session_state.stats["total"] += 1
            st.session_state.stats["timeout"] += 1
            st.session_state.streak = 0
            st.session_state.session.append({
                **q, "user": None, "ok": False, "time": TIME_LIMIT
            })
            st.rerun()

    # Show explanation
    if st.session_state.answered:
        st.markdown("---")
        sel = st.session_state.selected
        if sel == q["correct"]:
            st.success(f"✓ Richtig! Antwort: {q['correct']}")
        elif sel is None:
            st.warning(f"⏱ Zeit abgelaufen! Antwort: {q['correct']}")
        else:
            st.error(f"✗ Falsch. Richtige Antwort: {q['correct']}")

        st.markdown(q.get("explanation", ""))

        trap = q.get("trap_type", "")
        label = TRAP_LABELS.get(trap, trap)
        tip = TRAP_TIPS.get(trap, "")
        st.info(f"**Fehlertyp:** {label}\n\n**Tipp:** {tip}")

        # Next or finish
        if len(st.session_state.session) >= size:
            if st.button("📊 Ergebnis anzeigen", type="primary", use_container_width=True):
                st.session_state.screen = "results"
                st.rerun()
        else:
            if st.button("Nächste Frage →", type="primary", use_container_width=True):
                nq = get_next_question()
                if nq:
                    st.session_state.current_q = nq
                    st.session_state.answered = False
                    st.session_state.selected = None
                    st.session_state.start_time = time.time()
                st.rerun()

def show_results():
    session = st.session_state.session
    ok = sum(1 for q in session if q.get("ok"))
    pct = round((ok / len(session)) * 100) if session else 0
    avg_time = round(sum(q.get("time", 0) for q in session) / len(session)) if session else 0

    st.markdown("### 📊 Session beendet")

    # Score
    col1, col2, col3 = st.columns(3)
    col1.metric("Richtig", f"{pct}%")
    col2.metric("Score", f"{ok}/{len(session)}")
    col3.metric("Ø Zeit", f"{avg_time // 60}:{avg_time % 60:02d}")

    if len(session) == 20:
        if ok >= 17:
            st.success("🎯 Exzellent – Top-Percentile!")
        elif ok >= 14:
            st.success("📈 Stark – wettbewerbsfähig")
        elif ok >= 10:
            st.warning("✅ Bestanden – Luft nach oben")
        else:
            st.error(f"❌ Nicht bestanden ({ok}/20, min. 10)")

    # Question overview
    st.markdown("**Übersicht:**")
    for i, q in enumerate(session):
        icon = "✅" if q.get("ok") else "❌"
        src = "✦" if q.get("source") in ["EPSO Official", "Übungsfragen DE"] else "🤖"
        t = q.get("time", 0)
        st.caption(f"{icon} {src} {q.get('text', '')[:50]}... ({t // 60}:{t % 60:02d})")

    # Error analysis
    errors = [q for q in session if not q.get("ok")]
    if errors:
        st.markdown("---")
        st.markdown("**❌ Fehleranalyse:**")
        for q in errors:
            trap = q.get("trap_type", "")
            label = TRAP_LABELS.get(trap, trap)
            user_ans = q.get("user", "—")
            correct = q.get("correct", "?")
            user_stmt = next((o["statement"][:60] for o in q.get("options", []) if o["letter"] == user_ans), "—")
            corr_stmt = next((o["statement"][:60] for o in q.get("options", []) if o["letter"] == correct), "?")

            st.markdown(f"""
**{label}**
- ❌ Ihre Antwort ({user_ans}): _{user_stmt}..._
- ✅ Richtig ({correct}): _{corr_stmt}..._
- 💡 _{TRAP_TIPS.get(trap, '')}_
""")

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Neue Session", use_container_width=True):
            st.session_state.session = []
            st.session_state.screen = "question"
            nq = get_next_question()
            if nq:
                st.session_state.current_q = nq
                st.session_state.answered = False
                st.session_state.selected = None
                st.session_state.start_time = time.time()
            st.rerun()
    with col2:
        if st.button("🏠 Startseite", use_container_width=True):
            st.session_state.session = []
            st.session_state.screen = "home"
            st.rerun()

# ── Main Router ──
if st.session_state.screen == "home":
    show_home()
elif st.session_state.screen == "question":
    show_question()
elif st.session_state.screen == "results":
    show_results()
