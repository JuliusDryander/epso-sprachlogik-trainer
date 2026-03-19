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


# ── EU Design System Styling ──
# Official EU colors: Primary Blue #004494, Secondary Yellow #FFD617, Blue-75 #4073AF, Grey #404040
st.markdown("""
<style>
.stApp { max-width: 720px; margin: 0 auto; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; }
[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { display: none; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.eu-header {
    background: #004494; color: white;
    padding: 28px 28px 24px; margin-bottom: 20px;
    border-bottom: 4px solid #FFD617;
}
.eu-header h2 { color: white; margin: 0 0 2px; font-size: 22px; font-weight: bold; }
.eu-header p { color: rgba(255,255,255,0.75); margin: 0; font-size: 13px; }

.eu-card {
    background: white; border: 1px solid #e3e3e3;
    padding: 20px 24px; margin-bottom: 16px;
}
.eu-card-label {
    font-size: 11px; font-weight: bold; color: #004494;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-bottom: 12px; padding-bottom: 8px;
    border-bottom: 2px solid #FFD617; display: inline-block;
}

.eu-metrics { display: flex; gap: 1px; background: #e3e3e3; margin: 12px 0; }
.eu-metric { flex: 1; text-align: center; background: white; padding: 16px 8px; }
.eu-metric .num { font-size: 28px; font-weight: bold; line-height: 1; }
.eu-metric .label { font-size: 10px; color: #6b6b6b; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
.eu-green { color: #008a00; }
.eu-red { color: #da1e28; }
.eu-orange { color: #e07000; }
.eu-blue { color: #004494; }
.eu-grey { color: #404040; }

.eu-textbox {
    background: #f5f7fa; border-left: 4px solid #004494;
    padding: 20px 24px; margin: 16px 0;
    line-height: 1.85; font-size: 14.5px; color: #2d2d2d;
}

div[data-testid="stButton"] > button {
    width: 100%; text-align: left !important;
    padding: 14px 18px !important; border-radius: 0 !important;
    border: 1px solid #bfbfbf !important; border-left: 4px solid #bfbfbf !important;
    background: white !important; font-size: 14px !important;
    color: #2d2d2d !important; font-weight: normal !important;
    transition: all 0.12s ease !important; line-height: 1.5 !important;
    margin-bottom: 4px !important; font-family: Arial, sans-serif !important;
}
div[data-testid="stButton"] > button:hover {
    border-left-color: #004494 !important; background: #f0f4fa !important;
    color: #004494 !important; border-color: #004494 !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: #004494 !important; color: white !important;
    border: none !important; border-left: 4px solid #FFD617 !important;
    font-weight: bold !important; padding: 16px 24px !important;
    font-size: 15px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { background: #003776 !important; }

.eu-timer { text-align: center; font-size: 34px; font-weight: bold; font-variant-numeric: tabular-nums; }
.eu-timer-ok { color: #008a00; }
.eu-timer-warn { color: #e07000; }
.eu-timer-danger { color: #da1e28; animation: pulse 0.8s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

.eu-answer-correct { background:#defbe6; border:1px solid #008a00; border-left:4px solid #008a00; padding:14px 18px; margin:4px 0; font-size:14px; color:#044317; }
.eu-answer-wrong { background:#fff1f1; border:1px solid #da1e28; border-left:4px solid #da1e28; padding:14px 18px; margin:4px 0; font-size:14px; color:#750e13; }
.eu-answer-neutral { background:#f5f5f5; border:1px solid #e0e0e0; border-left:4px solid #e0e0e0; padding:14px 18px; margin:4px 0; font-size:14px; color:#8d8d8d; }

.eu-explain { background:white; border:1px solid #e3e3e3; border-top:3px solid #004494; padding:20px 24px; margin:16px 0; }
.eu-badge { display:inline-block; background:#FFD617; color:#2d2d2d; padding:4px 12px; font-size:12px; font-weight:bold; margin-bottom:10px; }
.eu-tip { background:#f0f4fa; border-left:3px solid #004494; padding:10px 14px; font-size:13px; color:#004494; margin-top:12px; }

.eu-src-badge { display:inline-block; padding:3px 10px; font-size:11px; font-weight:bold; letter-spacing:0.3px; }
.eu-src-verified { background:#dce8f5; color:#004494; }
.eu-src-ai { background:#f3e8ff; color:#6929c4; }

div[data-testid="stProgress"] > div > div { height:6px !important; border-radius:0 !important; }

.eu-result-row { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid #e8e8e8; font-size:13px; }
.eu-result-icon { width:22px; height:22px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:bold; flex-shrink:0; }
.eu-result-ok { background:#defbe6; color:#008a00; }
.eu-result-fail { background:#fff1f1; color:#da1e28; }

[data-testid="stMetric"] { display: none; }
</style>
""", unsafe_allow_html=True)

def get_next_question():
    available = [q for q in VERIFIED if q["id"] not in st.session_state.used_ids]
    if available and random.random() < 0.65:
        q = random.choice(available)
        st.session_state.used_ids.append(q["id"])
        return q
    api_key = st.session_state.get("api_key", "")
    if api_key:
        prev = ", ".join([q.get("text", "")[:25] for q in st.session_state.session[-3:]])
        return generate_ai_question(api_key, prev)
    if VERIFIED:
        return random.choice(VERIFIED)
    return None

def show_home():
    st.markdown("""
    <div class="eu-header">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px">
            <div style="font-size:28px">&#127466;&#127482;</div>
            <div><h2>Sprachlogisches Denken</h2><p>EPSO AD5 Auswahlverfahren &middot; Deutsch &middot; 1:45 pro Frage</p></div>
        </div>
        <div style="display:flex;gap:16px;font-size:12px;color:rgba(255,255,255,0.6)">
            <span>&#10022; 30 verifizierte Fragen</span><span>&#129302; KI-generierte Fragen</span><span>&#128202; 6 Fehlertypen</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("API-Key eingeben (optional, fuer KI-Fragen)"):
        api_key = st.text_input("Anthropic API Key", type="password", key="api_key_input", placeholder="sk-ant-...")
        if api_key:
            st.session_state.api_key = api_key
            st.success("KI-Fragen aktiviert")
        else:
            st.caption("Ohne Key: 30 verifizierte Fragen im Rotationsverfahren.")

    remaining = len([q for q in VERIFIED if q["id"] not in st.session_state.used_ids])
    current = st.session_state.session_size

    st.markdown("**Session konfigurieren**")
    cols = st.columns(4)
    for i, n in enumerate([5, 10, 15, 20]):
        with cols[i]:
            if st.button(str(n), key=f"size_{n}", type="primary" if current == n else "secondary"):
                st.session_state.session_size = n
                st.rerun()

    st.caption(f"{remaining}/{len(VERIFIED)} verifizierte Fragen verfuegbar")

    if st.button("Session starten", type="primary", use_container_width=True):
        st.session_state.session = []
        st.session_state.screen = "question"
        q = get_next_question()
        if q:
            st.session_state.current_q = q
            st.session_state.answered = False
            st.session_state.selected = None
            st.session_state.start_time = time.time()
        st.rerun()

    s = st.session_state.stats
    if s["total"] > 0:
        pct = round((s["correct"] / s["total"]) * 100)
        st.markdown(f"""
        <div class="eu-card">
            <div class="eu-card-label">Gesamtstatistik</div>
            <div class="eu-metrics">
                <div class="eu-metric"><div class="num eu-grey">{s['total']}</div><div class="label">Gesamt</div></div>
                <div class="eu-metric"><div class="num eu-green">{s['correct']}</div><div class="label">Richtig</div></div>
                <div class="eu-metric"><div class="num eu-red">{s['wrong']}</div><div class="label">Falsch</div></div>
                <div class="eu-metric"><div class="num eu-orange">{s['timeout']}</div><div class="label">Timeout</div></div>
                <div class="eu-metric"><div class="num eu-blue">{s['best_streak']}</div><div class="label">Streak</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(pct / 100, text=f"{pct}% Trefferquote")
        if s["traps"]:
            sorted_traps = sorted(s["traps"].items(), key=lambda x: x[1], reverse=True)
            html = '<div class="eu-card"><div class="eu-card-label" style="border-bottom-color:#da1e28;color:#da1e28">Schwachstellen</div>'
            for trap, count in sorted_traps[:5]:
                label = TRAP_LABELS.get(trap, trap)
                html += f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #e8e8e8;font-size:13px"><span style="color:#404040">{label}</span><span style="color:#da1e28;font-weight:bold">{count}x</span></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

def show_question():
    q = st.session_state.current_q
    if not q:
        st.session_state.screen = "home"
        st.rerun()
        return
    session = st.session_state.session
    size = st.session_state.session_size
    elapsed = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
    remaining = max(0, TIME_LIMIT - elapsed)
    s = st.session_state.stats

    if not st.session_state.answered:
        mins = remaining // 60
        secs = remaining % 60
        t_class = "eu-timer-ok" if remaining > 60 else ("eu-timer-warn" if remaining > 30 else "eu-timer-danger")
    else:
        mins = secs = 0
        t_class = ""

    streak_html = f' <span style="font-size:11px;background:#FFD617;padding:2px 6px;font-weight:bold">&#128293; {st.session_state.streak}</span>' if st.session_state.streak >= 3 else ""

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:2px solid #004494;margin-bottom:12px">
        <div style="font-size:14px;color:#6b6b6b">Frage <strong style="color:#004494;font-size:20px">{len(session)+1}</strong> / {size}</div>
        <div class="eu-timer {t_class}">{f'{mins}:{secs:02d}' if not st.session_state.answered else '&mdash;'}</div>
        <div style="font-size:14px"><span class="eu-green" style="font-weight:bold">{s['correct']}</span> <span style="color:#bfbfbf">|</span> <span class="eu-red" style="font-weight:bold">{s['wrong']+s['timeout']}</span>{streak_html}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered:
        pct = remaining / TIME_LIMIT
        color = "#008a00" if remaining > 60 else ("#e07000" if remaining > 30 else "#da1e28")
        st.markdown(f'<div style="height:3px;background:#e8e8e8;margin-bottom:16px"><div style="height:3px;width:{pct*100}%;background:{color};transition:width 1s linear"></div></div>', unsafe_allow_html=True)

    if q.get("source") in ["EPSO Official", "Übungsfragen DE"]:
        st.markdown(f'<span class="eu-src-badge eu-src-verified">&#10022; {q["source"]}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="eu-src-badge eu-src-ai">&#129302; KI-generiert</span>', unsafe_allow_html=True)

    st.markdown(f'<div class="eu-textbox">{q["text"]}</div>', unsafe_allow_html=True)

    is_incorrect = q.get("question_type") == "incorrect"
    if is_incorrect:
        st.markdown('<div style="background:#fff1f1;border-left:4px solid #da1e28;padding:10px 16px;font-weight:bold;color:#750e13;font-size:14px;margin-bottom:12px">Welche Aussage ist NICHT zutreffend?</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#f0f4fa;border-left:4px solid #004494;padding:10px 16px;font-weight:bold;color:#004494;font-size:14px;margin-bottom:12px">Welche Antwort kann am besten aus dem Text abgeleitet werden?</div>', unsafe_allow_html=True)

    for opt in q["options"]:
        letter = opt["letter"]
        statement = opt["statement"]
        is_selected = st.session_state.selected == letter
        is_correct_opt = letter == q["correct"]
        if st.session_state.answered:
            if is_correct_opt:
                st.markdown(f'<div class="eu-answer-correct"><strong>&#10003; {letter})</strong> {statement}</div>', unsafe_allow_html=True)
            elif is_selected:
                st.markdown(f'<div class="eu-answer-wrong"><strong>&#10007; {letter})</strong> {statement}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="eu-answer-neutral"><strong>{letter})</strong> {statement}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{letter})  {statement}", key=f"opt_{letter}"):
                elapsed_final = int(time.time() - st.session_state.start_time)
                st.session_state.selected = letter
                st.session_state.answered = True
                ok = letter == q["correct"]
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
                st.session_state.session.append({**q, "user": letter, "ok": ok, "time": min(elapsed_final, TIME_LIMIT)})
                st.rerun()

    if not st.session_state.answered and elapsed >= TIME_LIMIT:
        st.session_state.answered = True
        st.session_state.stats["total"] += 1
        st.session_state.stats["timeout"] += 1
        st.session_state.streak = 0
        st.session_state.session.append({**q, "user": None, "ok": False, "time": TIME_LIMIT})
        st.rerun()

    if st.session_state.answered:
        sel = st.session_state.selected
        if sel == q["correct"]:
            st.markdown('<div style="text-align:center;padding:14px;background:#defbe6;border-left:4px solid #008a00;margin:16px 0"><strong style="color:#008a00;font-size:16px">&#10003; Richtig!</strong></div>', unsafe_allow_html=True)
        elif sel is None:
            st.markdown('<div style="text-align:center;padding:14px;background:#fff8e1;border-left:4px solid #e07000;margin:16px 0"><strong style="color:#e07000;font-size:16px">&#9200; Zeit abgelaufen</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center;padding:14px;background:#fff1f1;border-left:4px solid #da1e28;margin:16px 0"><strong style="color:#da1e28;font-size:16px">&#10007; Falsch</strong> &mdash; Richtig: <strong>{q["correct"]}</strong></div>', unsafe_allow_html=True)

        trap = q.get("trap_type", "")
        label = TRAP_LABELS.get(trap, trap)
        tip = TRAP_TIPS.get(trap, "")
        show_tip = (not sel or sel != q["correct"]) and tip
        st.markdown(f"""
        <div class="eu-explain">
            <div class="eu-badge">{label}</div>
            <div style="font-size:14px;line-height:1.7;color:#2d2d2d">{q.get("explanation", "")}</div>
            {'<div class="eu-tip"><strong>Tipp:</strong> ' + tip + '</div>' if show_tip else ""}
        </div>
        """, unsafe_allow_html=True)

        if len(st.session_state.session) >= size:
            if st.button("Ergebnis anzeigen", type="primary", use_container_width=True):
                st.session_state.screen = "results"
                st.rerun()
        else:
            if st.button("Naechste Frage", type="primary", use_container_width=True):
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
    verified = sum(1 for q in session if q.get("source") in ["EPSO Official", "Übungsfragen DE"])
    emoji = "&#127919;" if pct >= 80 else ("&#128200;" if pct >= 60 else ("&#128170;" if pct >= 50 else "&#128260;"))

    st.markdown(f"""
    <div class="eu-header" style="text-align:center">
        <div style="font-size:48px;margin-bottom:8px">{emoji}</div>
        <h2>Session abgeschlossen</h2>
        <p>{verified} verifizierte + {len(session)-verified} KI-generierte Fragen</p>
    </div>
    """, unsafe_allow_html=True)

    pct_color = "eu-green" if pct >= 70 else ("eu-orange" if pct >= 50 else "eu-red")
    time_color = "eu-green" if avg_time <= 90 else "eu-orange"
    st.markdown(f"""
    <div class="eu-metrics">
        <div class="eu-metric"><div class="num {pct_color}">{pct}%</div><div class="label">Richtig</div></div>
        <div class="eu-metric"><div class="num eu-grey">{ok}/{len(session)}</div><div class="label">Score</div></div>
        <div class="eu-metric"><div class="num {time_color}">{avg_time//60}:{avg_time%60:02d}</div><div class="label">Zeit</div></div>
    </div>
    """, unsafe_allow_html=True)

    if len(session) == 20:
        if ok >= 17: st.success("Exzellent!")
        elif ok >= 14: st.success("Wettbewerbsfaehig")
        elif ok >= 10: st.warning("Bestanden (min. 10/20)")
        else: st.error(f"Nicht bestanden ({ok}/20)")

    items_html = '<div class="eu-card"><div class="eu-card-label">Uebersicht</div>'
    for q in session:
        ic = "eu-result-ok" if q.get("ok") else "eu-result-fail"
        sym = "&#10003;" if q.get("ok") else "&#10007;"
        t = q.get("time", 0)
        items_html += f'<div class="eu-result-row"><div class="eu-result-icon {ic}">{sym}</div><div style="flex:1;color:#404040">{q.get("text","")[:42]}...</div><div style="color:#bfbfbf;font-size:11px">{t//60}:{t%60:02d}</div></div>'
    items_html += '</div>'
    st.markdown(items_html, unsafe_allow_html=True)

    errors = [q for q in session if not q.get("ok")]
    if errors:
        err_html = '<div class="eu-card"><div class="eu-card-label" style="border-bottom-color:#da1e28;color:#da1e28">Fehleranalyse</div>'
        for q in errors:
            trap = q.get("trap_type", "")
            label = TRAP_LABELS.get(trap, trap)
            user_ans = q.get("user", "---")
            correct = q.get("correct", "?")
            user_stmt = next((o["statement"][:50] for o in q.get("options", []) if o["letter"] == user_ans), "---")
            corr_stmt = next((o["statement"][:50] for o in q.get("options", []) if o["letter"] == correct), "?")
            tip = TRAP_TIPS.get(trap, "")
            err_html += f'<div style="padding:12px 0;border-bottom:1px solid #e8e8e8"><div class="eu-badge" style="margin-bottom:6px">{label}</div><div style="font-size:12px;color:#da1e28">&#10007; {user_ans}: {user_stmt}...</div><div style="font-size:12px;color:#008a00">&#10003; {correct}: {corr_stmt}...</div><div style="font-size:11px;color:#6b6b6b;margin-top:4px">{tip}</div></div>'
        err_html += '</div>'
        st.markdown(err_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Neue Session", type="primary", use_container_width=True):
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
        if st.button("Startseite", use_container_width=True):
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
