Questo repository si pronone come benchmark per il task Chart to Table per il modello task-oriented DePlot e Gemini.
posiziona le tue immagini dentro data/pmc e dividile in basea alla difficoltà nelle directory easy, medium, hard e le tabelle in data_groundtruth/pmc e /easy o /medium o /hard
esegui ./chart_factory/_create_all_charts.sh per generare i grafici sintetici e salvare le rispettive tabelle
esegui ./gemini/ask_gemini.py per predire le immagini in data da gemini-2.5-flash le tabelle 
esegui ./deplot/inference.py per predire le immagini in data dal modello DePlot
Visualizza le predizioni tramite notebook visualize_predictions.ipynb e le metriche precision, recall, f1 relative a Relative Mapping Similarity.
Visualizza le metriche globali, per classe e per difficoltà nel notebook metric/results_metric.ipynb