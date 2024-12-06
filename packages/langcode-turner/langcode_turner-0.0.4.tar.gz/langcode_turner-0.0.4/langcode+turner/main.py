# coding:utf-8
import csv
class LangcodeTurner:

    id: str
    iso_639_2b: str | None
    iso_639_2t: str | None
    iso_639_3: str
    iso_639_1: str
    scope: str
    language_type: str
    ref_name: str
    comment: str | None

    def __init__(self, langcode: str,*type:str):
        with open("./iso.tab", "r", encoding="utf-8") as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                row = self.iso_table_row_reader(line)
                match type:
                    case "iso_639_1":
                        if row["iso_639_1"] == langcode:
                            self.write_in(row)
                            break
                    case "iso_639_3":
                        if row["iso_639_3"] == langcode:
                            self.write_in(row)
                            break
                    case "iso_639_2b":
                        if row["iso_639_2b"] == langcode:
                            self.write_in(row)
                            break
                    case "iso_639_2t":
                        if row["iso_639_2t"] == langcode:
                            self.write_in(row)
                            break
                    case "language":
                        if row["ref_name"] == langcode:
                            self.write_in(row)
                            break
                    case _:
                        match len(langcode):
                            case 3:
                                if row["iso_639_3"] == langcode:
                                    self.write_in(row)
                                    break
                            case 2:
                                if row["iso_639_1"] == langcode:
                                    self.write_in(row)
                                    break
                            case _:
                                if row["ref_name"] == langcode:
                                    self.write_in(row)
                                    break
                                raise ValueError("langcode is not valid")
    def write_in(self,row:dict):
        self.id = row["id"]
        self.iso_639_2b = row["iso_639_2b"]
        self.iso_639_2t = row["iso_639_2t"]
        self.iso_639_3 = row["iso_639_3"]
        self.iso_639_1 = row["iso_639_1"]
        self.scope = row["scope"]
        self.language_type = row["language_type"]
        self.ref_name = row["ref_name"]
        self.comment = row["comment"]

    def iso_table_row_reader(self,raw:list[str]):
        return {
            "id": raw[0],
            "iso_639_2b": raw[1],
            "iso_639_2t": raw[2],
            "iso_639_3": raw[0],
            "iso_639_1": raw[3],
            "scope": raw[4],
            "language_type": raw[5],
            "ref_name": raw[6],
            "comment": raw[7],
        }

