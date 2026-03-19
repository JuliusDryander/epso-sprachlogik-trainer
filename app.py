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
if "mode" not in st.session_state:
    st.session_state.mode = "mixed"  # "verified", "ai", "mixed"
if "session_used_ids" not in st.session_state:
    st.session_state.session_used_ids = []  # tracks IDs used in CURRENT session



# ══════════════════════════════════════════════════
# UI LAYER — Gamified EU Design
# ══════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --eu-blue: #004494;
    --eu-blue-dark: #003068;
    --eu-blue-light: #e8f0fe;
    --eu-yellow: #FFD617;
    --eu-green: #0d7c3f;
    --eu-red: #c0272d;
    --eu-orange: #d4620a;
    --eu-grey: #404040;
    --eu-grey-light: #f4f5f7;
    --radius: 12px;
}

.stApp { max-width: 680px; margin: 0 auto; font-family: 'Inter', Arial, sans-serif; }
[data-testid="stHeader"] { background: transparent; }
footer, #MainMenu { display: none; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

/* ── HERO HEADER ── */
.hero {
    background: linear-gradient(135deg, #003068 0%, #004494 60%, #1a5ab8 100%);
    color: white; padding: 32px 28px 24px; margin: -1rem -1rem 20px;
    position: relative; overflow: hidden;
}
.hero::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 4px; background: var(--eu-yellow);
}
.hero .stars {
    position: absolute; top: 16px; right: 20px; opacity: 0.08;
    font-size: 120px; line-height: 1;
}
.hero h1 { font-size: 26px; font-weight: 800; margin: 0 0 4px; letter-spacing: -0.5px; }
.hero .sub { color: rgba(255,255,255,0.65); font-size: 13px; margin: 0 0 16px; }
.hero .chips { display: flex; gap: 8px; flex-wrap: wrap; }
.hero .chip {
    background: rgba(255,255,255,0.12); backdrop-filter: blur(4px);
    padding: 5px 12px; border-radius: 20px; font-size: 11px;
    color: rgba(255,255,255,0.85); font-weight: 500;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ── CARDS ── */
.g-card {
    background: white; border-radius: var(--radius); padding: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);
    border: 1px solid #eef0f2; margin-bottom: 14px;
}
.g-card-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #8993a4; margin-bottom: 14px;
}

/* ── MODE SELECTOR (pill style) ── */
.mode-row { display: flex; gap: 0; background: var(--eu-grey-light); border-radius: 10px; padding: 3px; margin: 8px 0 16px; }
.mode-pill {
    flex: 1; text-align: center; padding: 10px 0; border-radius: 8px;
    font-size: 13px; font-weight: 600; color: #6b7280;
    cursor: pointer; transition: all 0.2s;
}
.mode-pill.active {
    background: var(--eu-blue); color: white;
    box-shadow: 0 2px 8px rgba(0,68,148,0.3);
}

/* ── SIZE SELECTOR ── */
.size-row { display: flex; gap: 6px; margin: 8px 0 16px; }
.size-pill {
    flex: 1; text-align: center; padding: 10px 0; border-radius: 8px;
    font-size: 15px; font-weight: 700; color: #8993a4; background: var(--eu-grey-light);
    border: 2px solid transparent; cursor: pointer; transition: all 0.15s;
}
.size-pill.active {
    background: white; color: var(--eu-blue);
    border-color: var(--eu-blue); box-shadow: 0 0 0 3px rgba(0,68,148,0.1);
}

/* ── METRICS (gamified) ── */
.g-metrics { display: flex; gap: 8px; margin: 12px 0; }
.g-stat {
    flex: 1; text-align: center; background: var(--eu-grey-light);
    border-radius: 10px; padding: 14px 6px;
    transition: transform 0.15s;
}
.g-stat:hover { transform: translateY(-2px); }
.g-stat .num { font-size: 24px; font-weight: 800; line-height: 1; }
.g-stat .label { font-size: 9px; color: #8993a4; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
.g-green { color: var(--eu-green); }
.g-red { color: var(--eu-red); }
.g-orange { color: var(--eu-orange); }
.g-blue { color: var(--eu-blue); }

/* ── BUTTONS (answer options) ── */
div[data-testid="stButton"] > button {
    width: 100%; text-align: left !important;
    padding: 16px 20px !important; border-radius: 10px !important;
    border: 2px solid #e5e7eb !important;
    background: white !important; font-size: 14px !important;
    color: #1f2937 !important; font-weight: 500 !important;
    transition: all 0.15s ease !important; line-height: 1.55 !important;
    margin-bottom: 6px !important; font-family: 'Inter', Arial, sans-serif !important;
    min-height: 68px !important; display: flex !important; align-items: center !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--eu-blue) !important; background: var(--eu-blue-light) !important;
    color: var(--eu-blue) !important; transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,68,148,0.1);
}

/* Primary button */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #003068 0%, #004494 100%) !important;
    color: white !important; border: none !important;
    font-weight: 700 !important; padding: 16px 24px !important;
    font-size: 15px !important; min-height: 52px !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 14px rgba(0,68,148,0.25) !important;
    letter-spacing: 0.3px;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0,68,148,0.35) !important;
}

/* ── TIMER ── */
.g-timer-bar {
    position: sticky; top: 0; z-index: 999;
    background: white; padding: 10px 0 0;
    margin: -1rem -1rem 14px; padding-left: 1rem; padding-right: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06); border-radius: 0 0 12px 12px;
}
.g-timer-row {
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 8px;
}
.g-timer-num {
    font-size: 36px; font-weight: 800; font-variant-numeric: tabular-nums;
    letter-spacing: -1px;
}
.g-timer-ok { color: var(--eu-green); }
.g-timer-warn { color: var(--eu-orange); }
.g-timer-danger { color: var(--eu-red); animation: pulse 0.8s ease-in-out infinite; }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.35; } }
.g-progress {
    height: 4px; background: #eef0f2; border-radius: 2px; margin-bottom: 10px; overflow: hidden;
}
.g-progress-fill { height: 100%; border-radius: 2px; transition: width 1s linear; }

/* ── ANSWER STATES ── */
.g-ans {
    padding: 16px 20px; margin: 5px 0; border-radius: 10px;
    font-size: 14px; min-height: 68px; display: flex; align-items: center;
    line-height: 1.55; font-weight: 500;
}
.g-ans-correct { background: #ecfdf5; border: 2px solid var(--eu-green); color: #065f46; }
.g-ans-wrong { background: #fef2f2; border: 2px solid var(--eu-red); color: #7f1d1d; }
.g-ans-neutral { background: #f9fafb; border: 1px solid #e5e7eb; color: #9ca3af; }

/* ── EXPLANATION BOX ── */
.g-explain {
    background: white; border-radius: var(--radius);
    border: 1px solid #eef0f2; padding: 20px; margin: 16px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.g-explain-badge {
    display: inline-block; background: var(--eu-yellow); color: #1f2937;
    padding: 4px 12px; border-radius: 6px; font-size: 11px;
    font-weight: 700; margin-bottom: 10px; letter-spacing: 0.3px;
}
.g-explain-tip {
    background: var(--eu-blue-light); border-left: 3px solid var(--eu-blue);
    padding: 10px 14px; border-radius: 0 8px 8px 0;
    font-size: 13px; color: var(--eu-blue); margin-top: 12px; font-weight: 500;
}

/* ── BADGES ── */
.g-badge {
    display: inline-block; padding: 4px 10px; border-radius: 6px;
    font-size: 11px; font-weight: 600;
}
.g-badge-verified { background: var(--eu-blue-light); color: var(--eu-blue); }
.g-badge-ai { background: #f3e8ff; color: #7c3aed; }

/* ── STREAK BADGE ── */
.g-streak {
    display: inline-flex; align-items: center; gap: 3px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: white; padding: 3px 8px; border-radius: 6px;
    font-size: 11px; font-weight: 700;
}

/* ── RESULT ITEMS ── */
.g-result-row {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 0; border-bottom: 1px solid #f3f4f6; font-size: 13px;
}
.g-result-dot {
    width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.g-dot-ok { background: var(--eu-green); }
.g-dot-fail { background: var(--eu-red); }

/* ── XP BAR ── */
.g-xp-bar {
    background: #eef0f2; border-radius: 6px; height: 8px; overflow: hidden; margin: 6px 0;
}
.g-xp-fill {
    height: 100%; border-radius: 6px;
    background: linear-gradient(90deg, var(--eu-blue), #1a5ab8);
    transition: width 0.5s ease;
}

/* Override Streamlit progress */
div[data-testid="stProgress"] > div > div { height: 8px !important; border-radius: 6px !important; }
[data-testid="stMetric"] { display: none; }

/* ── HOME BUTTON ── */
.g-home-btn {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 12px; color: #8993a4; font-weight: 600;
    cursor: pointer; padding: 4px 0; margin-bottom: 4px;
}
.g-home-btn:hover { color: var(--eu-blue); }

/* ── RESULT HEADER ── */
.g-result-hero {
    background: linear-gradient(135deg, #003068 0%, #004494 60%, #1a5ab8 100%);
    color: white; text-align: center; padding: 36px 24px 28px;
    margin: -1rem -1rem 20px; position: relative;
}
.g-result-hero::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 4px; background: var(--eu-yellow);
}
.g-result-hero .big { font-size: 56px; font-weight: 800; }
.g-result-hero h2 { font-size: 20px; font-weight: 700; color: white; margin: 4px 0 0; }
.g-result-hero .sub { color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ──
def get_next_question():
    mode = st.session_state.mode
    used_in_session = st.session_state.session_used_ids
    api_key = st.session_state.get("api_key", "")
    if mode == "ai":
        if api_key:
            prev = ", ".join([q.get("text", "")[:25] for q in st.session_state.session[-3:]])
            q = generate_ai_question(api_key, prev)
            if q: st.session_state.session_used_ids.append(q["id"])
            return q
        else:
            st.error("Kein API-Key. Bitte auf der Startseite eingeben.")
            return None
    if mode == "verified":
        available = [q for q in VERIFIED if q["id"] not in used_in_session]
        if not available: available = VERIFIED[:]
        q = random.choice(available)
        st.session_state.session_used_ids.append(q["id"])
        st.session_state.used_ids.append(q["id"])
        return q
    # mixed
    available = [q for q in VERIFIED if q["id"] not in used_in_session]
    if available and (random.random() < 0.65 or not api_key):
        q = random.choice(available)
        st.session_state.session_used_ids.append(q["id"])
        st.session_state.used_ids.append(q["id"])
        return q
    if api_key:
        prev = ", ".join([q.get("text", "")[:25] for q in st.session_state.session[-3:]])
        q = generate_ai_question(api_key, prev)
        if q: st.session_state.session_used_ids.append(q["id"])
        return q
    if VERIFIED:
        q = random.choice(VERIFIED)
        return q
    return None

def start_session():
    st.session_state.session = []
    st.session_state.session_used_ids = []
    st.session_state.screen = "question"
    q = get_next_question()
    if q:
        st.session_state.current_q = q
        st.session_state.answered = False
        st.session_state.selected = None
        st.session_state.start_time = time.time()
    st.rerun()

def go_home():
    st.session_state.screen = "home"
    st.session_state.session = []
    st.session_state.session_used_ids = []
    st.rerun()

# ══════════════════════════════════════════════════
# HOME SCREEN
# ══════════════════════════════════════════════════
def show_home():
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="stars">&#9734;</div>
        <h1>Sprachlogisches Denken</h1>
        <p class="sub">EPSO AD5 Auswahlverfahren &middot; Verbal Reasoning &middot; Deutsch</p>
        <div class="chips">
            <span class="chip">&#9733; 30 verifizierte Fragen</span>
            <span class="chip">&#9881; KI-generierte Fragen</span>
            <span class="chip">1:45 pro Frage</span>
            <span class="chip">6 Fehlertypen</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # API Key detection
    secret_key = None
    try:
        secret_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    except Exception:
        pass
    if secret_key:
        st.session_state.api_key = secret_key
    else:
        with st.expander("API-Key eingeben (optional)"):
            api_key = st.text_input("Anthropic API Key", type="password", key="api_key_input", placeholder="sk-ant-...")
            if api_key:
                st.session_state.api_key = api_key

    has_api = bool(st.session_state.get("api_key"))

    # Config card
    remaining = len([q for q in VERIFIED if q["id"] not in st.session_state.used_ids])
    current_mode = st.session_state.mode
    current_size = st.session_state.session_size

    # Mode selector
    st.markdown('<div class="g-card"><div class="g-card-label">Trainingsmodus</div>', unsafe_allow_html=True)
    mode_cols = st.columns(3)
    modes = [("verified", "Verifiziert"), ("ai", "Nur KI"), ("mixed", "Gemischt")]
    for i, (mk, ml) in enumerate(modes):
        with mode_cols[i]:
            disabled = (mk == "ai" and not has_api)
            tp = "primary" if current_mode == mk else "secondary"
            label = ml + (" *" if mk == "ai" and not has_api else "")
            if st.button(label, key=f"m_{mk}", type=tp, disabled=disabled, use_container_width=True):
                st.session_state.mode = mk
                st.rerun()

    mode_desc = {"verified": "30 handgepruefte EPSO-Fragen", "ai": "Unbegrenzte neue Fragen via Claude", "mixed": "Beste Mischung aus beidem"}
    st.markdown(f'<div style="font-size:12px;color:#8993a4;margin-top:4px">{mode_desc.get(current_mode, "")}</div></div>', unsafe_allow_html=True)

    # Size selector
    st.markdown('<div class="g-card"><div class="g-card-label">Anzahl Fragen</div>', unsafe_allow_html=True)
    size_html = '<div class="size-row">'
    for n in [5, 10, 15, 20]:
        active = "active" if n == current_size else ""
        size_html += f'<div class="size-pill {active}">{n}</div>'
    size_html += '</div></div>'
    st.markdown(size_html, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, n in enumerate([5, 10, 15, 20]):
        with cols[i]:
            if st.button(str(n), key=f"s_{n}", type="primary" if current_size == n else "secondary"):
                st.session_state.session_size = n
                st.rerun()

    # EPSO benchmark info
    if current_size == 20:
        st.markdown('<div style="background:#e8f0fe;border-radius:8px;padding:10px 14px;font-size:12px;color:#004494;margin-bottom:14px"><strong>EPSO-Simulation:</strong> 20 Fragen = echte Testbedingungen. Bestehensgrenze: 10/20.</div>', unsafe_allow_html=True)

    # Start
    if st.button("Session starten", type="primary", use_container_width=True):
        start_session()

    # Stats
    s = st.session_state.stats
    if s["total"] > 0:
        pct = round((s["correct"] / s["total"]) * 100)
        level = pct // 10
        level_names = {0:"Anfaenger",1:"Anfaenger",2:"Anfaenger",3:"Lernend",4:"Lernend",5:"Bestehend",6:"Gut",7:"Stark",8:"Exzellent",9:"Top",10:"Meister"}
        st.markdown(f"""
        <div class="g-card">
            <div class="g-card-label">Dein Fortschritt</div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <div style="font-size:14px;font-weight:700;color:#1f2937">Level {level} &middot; {level_names.get(level, "")}</div>
                <div style="font-size:14px;font-weight:700;color:var(--eu-blue)">{pct}%</div>
            </div>
            <div class="g-xp-bar"><div class="g-xp-fill" style="width:{pct}%"></div></div>
            <div class="g-metrics">
                <div class="g-stat"><div class="num" style="color:#1f2937">{s['total']}</div><div class="label">Fragen</div></div>
                <div class="g-stat"><div class="num g-green">{s['correct']}</div><div class="label">Richtig</div></div>
                <div class="g-stat"><div class="num g-red">{s['wrong']}</div><div class="label">Falsch</div></div>
                <div class="g-stat"><div class="num g-blue">{s['best_streak']}</div><div class="label">Streak</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if s["traps"]:
            sorted_traps = sorted(s["traps"].items(), key=lambda x: x[1], reverse=True)
            html = '<div class="g-card"><div class="g-card-label">Schwachstellen</div>'
            for trap, count in sorted_traps[:5]:
                label = TRAP_LABELS.get(trap, trap)
                total_wrong = s["wrong"]
                pct_trap = round(count / total_wrong * 100) if total_wrong else 0
                html += f'<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #f3f4f6"><span style="font-size:13px;color:#4b5563">{label}</span><div style="display:flex;align-items:center;gap:8px"><div style="width:60px;height:4px;background:#fee2e2;border-radius:2px"><div style="width:{pct_trap}%;height:4px;background:var(--eu-red);border-radius:2px"></div></div><span style="font-size:13px;font-weight:700;color:var(--eu-red)">{count}</span></div></div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# QUESTION SCREEN
# ══════════════════════════════════════════════════
def show_question():
    if st.button("< Abbrechen", key="home_from_q"):
        go_home()

    q = st.session_state.current_q
    if not q:
        go_home()
        return

    session = st.session_state.session
    size = st.session_state.session_size
    elapsed = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
    remaining = max(0, TIME_LIMIT - elapsed)
    s = st.session_state.stats

    if not st.session_state.answered:
        mins = remaining // 60
        secs = remaining % 60
        tc = "g-timer-ok" if remaining > 60 else ("g-timer-warn" if remaining > 30 else "g-timer-danger")
    else:
        mins = secs = 0
        tc = ""

    streak_html = f'<span class="g-streak">&#9889; {st.session_state.streak}</span>' if st.session_state.streak >= 3 else ""
    pct_done = (len(session)) / size * 100

    # Sticky timer bar
    progress_color = "var(--eu-green)" if remaining > 60 else ("var(--eu-orange)" if remaining > 30 else "var(--eu-red)")
    timer_pct = remaining / TIME_LIMIT * 100 if not st.session_state.answered else 0
    st.markdown(f"""
    <div class="g-timer-bar">
        <div class="g-timer-row">
            <div>
                <span style="font-size:12px;color:#8993a4">Frage</span>
                <span style="font-size:20px;font-weight:800;color:var(--eu-blue);margin-left:4px">{len(session)+1}</span>
                <span style="font-size:12px;color:#8993a4">/ {size}</span>
            </div>
            <div class="g-timer-num {tc}">{f'{mins}:{secs:02d}' if not st.session_state.answered else '&mdash;'}</div>
            <div style="display:flex;align-items:center;gap:8px">
                <span style="font-size:14px"><span class="g-green" style="font-weight:700">{s['correct']}</span><span style="color:#d1d5db;margin:0 3px">:</span><span class="g-red" style="font-weight:700">{s['wrong']+s['timeout']}</span></span>
                {streak_html}
            </div>
        </div>
        <div class="g-progress"><div class="g-progress-fill" style="width:{timer_pct}%;background:{progress_color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # Source badge
    if q.get("source") in ["EPSO Official", "Übungsfragen DE"]:
        st.markdown(f'<span class="g-badge g-badge-verified">&#10022; {q["source"]}</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="g-badge g-badge-ai">&#9881; KI-generiert</span>', unsafe_allow_html=True)

    # Text
    st.markdown(f"""
    <div style="background:var(--eu-grey-light);border-left:4px solid var(--eu-blue);
        border-radius:0 var(--radius) var(--radius) 0;padding:20px 24px;margin:12px 0;
        line-height:1.85;font-size:14.5px;color:#1f2937">{q['text']}</div>
    """, unsafe_allow_html=True)

    # Question
    is_incorrect = q.get("question_type") == "incorrect"
    if is_incorrect:
        st.markdown('<div style="background:#fef2f2;border-radius:8px;padding:10px 16px;font-weight:700;color:var(--eu-red);font-size:14px;margin-bottom:12px">&#9888; Welche Aussage ist NICHT zutreffend?</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:var(--eu-blue-light);border-radius:8px;padding:10px 16px;font-weight:600;color:var(--eu-blue);font-size:14px;margin-bottom:12px">Welche Antwort kann am besten aus dem Text abgeleitet werden?</div>', unsafe_allow_html=True)

    # Options
    for opt in q["options"]:
        letter = opt["letter"]
        statement = opt["statement"]
        is_sel = st.session_state.selected == letter
        is_corr = letter == q["correct"]

        if st.session_state.answered:
            if is_corr:
                st.markdown(f'<div class="g-ans g-ans-correct"><strong>&#10003; {letter})</strong>&nbsp;&nbsp;{statement}</div>', unsafe_allow_html=True)
            elif is_sel:
                st.markdown(f'<div class="g-ans g-ans-wrong"><strong>&#10007; {letter})</strong>&nbsp;&nbsp;{statement}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="g-ans g-ans-neutral"><strong>{letter})</strong>&nbsp;&nbsp;{statement}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{letter})  {statement}", key=f"opt_{letter}"):
                elapsed_f = int(time.time() - st.session_state.start_time)
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
                st.session_state.session.append({**q, "user": letter, "ok": ok, "time": min(elapsed_f, TIME_LIMIT)})
                st.rerun()

    # Timeout
    if not st.session_state.answered and elapsed >= TIME_LIMIT:
        st.session_state.answered = True
        st.session_state.stats["total"] += 1
        st.session_state.stats["timeout"] += 1
        st.session_state.streak = 0
        st.session_state.session.append({**q, "user": None, "ok": False, "time": TIME_LIMIT})
        st.rerun()

    # Auto-refresh
    if not st.session_state.answered:
        try:
            from streamlit_autorefresh import st_autorefresh
            st_autorefresh(interval=1000, limit=TIME_LIMIT, key="timer_refresh")
        except ImportError:
            import streamlit.components.v1 as components
            components.html('<script>setTimeout(function(){window.parent.location.reload()},1100);</script>', height=0)

    # Explanation
    if st.session_state.answered:
        sel = st.session_state.selected
        if sel == q["correct"]:
            st.markdown('<div style="text-align:center;padding:16px;background:#ecfdf5;border-radius:var(--radius);margin:16px 0"><span style="font-size:24px">&#10003;</span><br><strong style="color:var(--eu-green);font-size:16px">Richtig!</strong></div>', unsafe_allow_html=True)
        elif sel is None:
            st.markdown('<div style="text-align:center;padding:16px;background:#fffbeb;border-radius:var(--radius);margin:16px 0"><span style="font-size:24px">&#9200;</span><br><strong style="color:var(--eu-orange);font-size:16px">Zeit abgelaufen</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center;padding:16px;background:#fef2f2;border-radius:var(--radius);margin:16px 0"><span style="font-size:24px">&#10007;</span><br><strong style="color:var(--eu-red);font-size:16px">Falsch</strong> &mdash; Richtig war <strong>{q["correct"]}</strong></div>', unsafe_allow_html=True)

        trap = q.get("trap_type", "")
        label = TRAP_LABELS.get(trap, trap)
        tip = TRAP_TIPS.get(trap, "")
        show_tip = (not sel or sel != q["correct"]) and tip

        st.markdown(f"""
        <div class="g-explain">
            <div class="g-explain-badge">{label}</div>
            <div style="font-size:14px;line-height:1.7;color:#374151">{q.get("explanation", "")}</div>
            {'<div class="g-explain-tip"><strong>Tipp:</strong> ' + tip + '</div>' if show_tip else ''}
        </div>
        """, unsafe_allow_html=True)

        if len(st.session_state.session) >= size:
            if st.button("Ergebnis anzeigen", type="primary", use_container_width=True):
                st.session_state.screen = "results"
                st.rerun()
        else:
            if st.button("Weiter", type="primary", use_container_width=True):
                nq = get_next_question()
                if nq:
                    st.session_state.current_q = nq
                    st.session_state.answered = False
                    st.session_state.selected = None
                    st.session_state.start_time = time.time()
                st.rerun()

# ══════════════════════════════════════════════════
# RESULTS SCREEN
# ══════════════════════════════════════════════════
def show_results():
    session = st.session_state.session
    ok = sum(1 for q in session if q.get("ok"))
    pct = round((ok / len(session)) * 100) if session else 0
    avg_time = round(sum(q.get("time", 0) for q in session) / len(session)) if session else 0
    verified = sum(1 for q in session if q.get("source") in ["EPSO Official", "Übungsfragen DE"])

    grade = "&#127942;" if pct >= 90 else ("&#9733;" if pct >= 70 else ("&#9650;" if pct >= 50 else "&#8635;"))
    grade_text = "Hervorragend!" if pct >= 90 else ("Stark!" if pct >= 70 else ("Bestanden" if pct >= 50 else "Weiter ueben"))

    st.markdown(f"""
    <div class="g-result-hero">
        <div class="big">{grade}</div>
        <div style="font-size:48px;font-weight:800;margin:4px 0">{pct}%</div>
        <h2>{grade_text}</h2>
        <div class="sub">{ok}/{len(session)} richtig &middot; &#216; {avg_time//60}:{avg_time%60:02d} pro Frage</div>
    </div>
    """, unsafe_allow_html=True)

    # Score cards
    st.markdown(f"""
    <div class="g-metrics">
        <div class="g-stat"><div class="num g-green">{ok}</div><div class="label">Richtig</div></div>
        <div class="g-stat"><div class="num g-red">{len(session)-ok}</div><div class="label">Falsch</div></div>
        <div class="g-stat"><div class="num g-blue">{verified}</div><div class="label">Verifiziert</div></div>
        <div class="g-stat"><div class="num" style="color:#7c3aed">{len(session)-verified}</div><div class="label">KI</div></div>
    </div>
    """, unsafe_allow_html=True)

    if len(session) == 20:
        if ok >= 17: st.success("Exzellent!")
        elif ok >= 14: st.success("Wettbewerbsfaehig")
        elif ok >= 10: st.warning("Bestanden (min. 10/20)")
        else: st.error(f"Nicht bestanden ({ok}/20)")

    # Per-question results
    items_html = '<div class="g-card"><div class="g-card-label">Alle Fragen</div>'
    for i, q in enumerate(session):
        dot = "g-dot-ok" if q.get("ok") else "g-dot-fail"
        t = q.get("time", 0)
        items_html += f'<div class="g-result-row"><div style="font-size:12px;color:#8993a4;width:20px">{i+1}</div><div class="g-result-dot {dot}"></div><div style="flex:1;color:#4b5563">{q.get("text","")[:45]}...</div><div style="color:#d1d5db;font-size:11px;font-variant-numeric:tabular-nums">{t//60}:{t%60:02d}</div></div>'
    items_html += '</div>'
    st.markdown(items_html, unsafe_allow_html=True)

    # Error analysis
    errors = [q for q in session if not q.get("ok")]
    if errors:
        err_html = '<div class="g-card"><div class="g-card-label" style="color:var(--eu-red)">Fehleranalyse</div>'
        for q in errors:
            trap = q.get("trap_type", "")
            label = TRAP_LABELS.get(trap, trap)
            user_ans = q.get("user", "---")
            correct = q.get("correct", "?")
            user_stmt = next((o["statement"][:50] for o in q.get("options", []) if o["letter"] == user_ans), "---")
            corr_stmt = next((o["statement"][:50] for o in q.get("options", []) if o["letter"] == correct), "?")
            tip = TRAP_TIPS.get(trap, "")
            err_html += f'<div style="padding:14px 0;border-bottom:1px solid #f3f4f6"><div class="g-explain-badge" style="margin-bottom:8px">{label}</div><div style="font-size:12px;color:var(--eu-red);margin-bottom:2px">&#10007; {user_ans}: {user_stmt}...</div><div style="font-size:12px;color:var(--eu-green);margin-bottom:4px">&#10003; {correct}: {corr_stmt}...</div><div style="font-size:11px;color:#8993a4">{tip}</div></div>'
        err_html += '</div>'
        st.markdown(err_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Neue Session", type="primary", use_container_width=True):
            start_session()
    with col2:
        if st.button("Startseite", use_container_width=True):
            go_home()

# ── Main Router ──
if st.session_state.screen == "home":
    show_home()
elif st.session_state.screen == "question":
    show_question()
elif st.session_state.screen == "results":
    show_results()
