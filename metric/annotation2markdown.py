import json
import os

def json_to_markdown(file_path):
    """
    Legge un file JSON contenente i dati di un grafico e genera due rappresentazioni 
    tabellari testuali (formato originale e trasposto).

    La funzione estrae dinamicamente il titolo, le etichette degli assi 
    (x_axis_label, y_axis_label) e i punti dati. Implementa una logica specifica 
    per la gestione delle serie:
    - Se esiste una singola serie predefinita ("Main"), utilizza l'etichetta 
      indicata dal capo categorical_axis per nominare la riga/colonna dei valori
      se questa non esiste in base all'asse Y.
    - Se esistono serie multiple, utilizza i nomi effettivi delle serie (series_name) 
      per differenziare le righe/colonne.

    I dati vengono incrociati tramite una mappa (dizionario lookup) basata su 
    chiavi (serie, valore X). Questo garantisce che la tabella venga costruita 
    correttamente anche se i punti nel JSON non sono in ordine o se mancano 
    alcuni valori per determinate serie.

    Argomenti:
        file_path (str): Il percorso del file JSON da analizzare.

    Ritorna:
        tuple: Una tupla di due elementi (original_table, transposed_table).
            - original_table (str): Etichette X sulle colonne, serie/valori sulle righe.
            - transposed_table (str): Etichette X sulle righe, serie/valori sulle colonne.
            Se il file non esiste o non è valido, ritorna stringhe di errore.
    """
    file_path = str(file_path)
    if not os.path.exists(file_path):
        return f"Errore: Il file '{file_path}' non esiste.", ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return "Errore: Il file non contiene un JSON valido.", ""
    except Exception as e:
        return f"Errore durante la lettura del file: {e}", ""
        
    title = data.get("chart_title", "Unknown Entity")
    raw_x_label = data.get("x_axis_label") or "X-Axis"
    raw_y_label = data.get("y_axis_label") or "Value"
    cat_axis = str(data.get("categorical_axis", "x")).strip().lower()
    swap_axes = (cat_axis == "y")
    if swap_axes:
        x_label = raw_y_label
        y_label = raw_x_label
    else:
        x_label = raw_x_label
        y_label = raw_y_label
    data_points = data.get("data_points", [])
    
    x_values = []
    series_names = []
    lookup = {}
    
    for point in data_points:
        if swap_axes:
            x = str(point.get("y_value", ""))
            y = str(point.get("x_value", ""))
        else:
            x = str(point.get("x_value", ""))
            y = str(point.get("y_value", ""))
            
        s = str(point.get("series_name", "Main"))
        
        if x not in x_values:
            x_values.append(x)
        if s not in series_names:
            series_names.append(s)
            
        lookup[(s, x)] = y

    is_single_main = len(series_names) == 1 or series_names[0] == "Main"
    print(len(series_names))
    lookup = {}
    for point in data_points:
        x = str(point.get("x_value", ""))
        s = str(point.get("series_name", "Main"))
        y = str(point.get("y_value", ""))
        lookup[(s, x)] = y

    # --- COSTRUZIONE TABELLA ORIGINALE ---
    title_row = f"TITLE | {title}"
    header_row = f" {x_label} | " + " | ".join(x_values)
    
    original_rows = [title_row, header_row]
    for s in series_names:
        row_label = y_label if is_single_main else s
        row_data = [f" {row_label}"]
        for x in x_values:
            row_data.append(lookup.get((s, x), "0")) 
        original_rows.append(" | ".join(row_data))
        
    original_table = "\n".join(original_rows)
    
    # --- COSTRUZIONE TABELLA TRASPOSTA ---
    transposed_headers = [f" {x_label}"]
    for s in series_names:
        transposed_headers.append(y_label if is_single_main else s)
        
    transposed_header_str = " | ".join(transposed_headers)
    transposed_rows_list = [title_row, transposed_header_str]
    
    for x in x_values:
        row_data = [f" {x}"]
        for s in series_names:
            row_data.append(lookup.get((s, x), "0"))
        transposed_rows_list.append(" | ".join(row_data))
        
    transposed_table = "\n".join(transposed_rows_list)
    
    return (original_table, transposed_table)

if __name__ == "__main__":
    print(json_to_markdown("predictions/Gemini/pmc/bar/hard/PMC12681856_fig_5_crop_46.json")[0])
    print(json_to_markdown("predictions/Gemini/pmc/bar/hard/PMC12681856_fig_5_crop_46.json")[1])