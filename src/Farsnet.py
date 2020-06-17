import sqlite3
import enum


class SqlLiteDbUtility:
    connection = None

    def getConnection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('farsnet3.sqlite3')
        return self.connection


class SynsetService:
    @staticmethod
    def getSynsetsByWord(searchStyle, searchKeyword):
        results = []
        sql = "SELECT id, pos, semanticCategory, example, gloss, nofather, noMapping FROM synset WHERE synset.id IN (SELECT synset.id as synset_id FROM word INNER JOIN sense ON sense.word = word.id INNER JOIN synset ON sense.synset = synset.id LEFT OUTER JOIN value ON value.word = word.id WHERE word.search_value @SearchStyle '@SearchValue' OR (value.search_value) @SearchStyle '@SearchValue')  OR synset.id IN (SELECT sense.synset AS synset_id FROM sense INNER JOIN sense_relation ON sense.id = sense_relation.sense INNER JOIN sense AS sense_2 ON sense_2.id = sense_relation.sense2 INNER JOIN word ON sense_2.word = word.id WHERE sense_relation.type =  'Refer-to' AND word.search_value LIKE  '@SearchValue') OR synset.id IN (SELECT sense_2.synset AS synset_id FROM sense INNER JOIN sense_relation ON sense.id = sense_relation.sense INNER JOIN sense AS sense_2 ON sense_2.id = sense_relation.sense2 INNER JOIN word ON sense.word = word.id WHERE sense_relation.type =  'Refer-to' AND word.search_value LIKE  '@SearchValue')"
        searchKeyword = SynsetService.SecureValue(SynsetService.NormalValue(searchKeyword))
        if searchStyle == "LIKE" or searchStyle == "START" or searchStyle == "END":
            sql = sql.replace("@SearchStyle", "LIKE")
            if searchStyle == "LIKE":
                searchKeyword = "%" + searchKeyword + "%"
            if searchStyle == "START":
                searchKeyword += "%"
            if searchStyle == "END":
                searchKeyword = "%" + searchKeyword
        if searchStyle == "EXACT":
            sql = sql.replace("@SearchStyle", "=")
        sql = sql.replace("@SearchValue", searchKeyword)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(Synset(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return results

    @staticmethod
    def getAllSynsets():
        results = []
        sql = "SELECT id, pos, semanticCategory, example, gloss, nofather, noMapping FROM synset "
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(Synset(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return results

    @staticmethod
    def getSynsetById(synsetId):
        results = []
        sql = "SELECT id, pos, semanticCategory, example, gloss, nofather, noMapping FROM synset WHERE id=" + str(
            synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(Synset(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return results

    @staticmethod
    def getSynsetRelationsById(synsetId):
        results = []
        sql = "SELECT id, type, synsetWords1, synsetWords2, synset, synset2, reverse_type FROM synset_relation WHERE synset=" + str(
            synsetId) + " OR synset2=" + str(synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SynsetRelation(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        resultsArr = []
        for i in range(0, len(results)):
            temp = results[i]
            if temp.synsetId1 != synsetId:
                type = temp.type
                synsetId2 = temp.synsetId2
                synsetId1 = temp.synsetId1
                synsetWords2 = temp.synsetWords2
                synsetWords1 = temp.synsetWords1
                reverseType = temp.reverseType
                temp.reverseType = type
                temp.synsetId1 = synsetId2
                temp.synsetId2 = synsetId1
                temp.synsetWords1 = synsetWords2
                temp.synsetWords2 = synsetWords1
                temp.type = reverseType
            resultsArr.append(temp)
        return resultsArr

    @staticmethod
    def getSynsetRelationsByType(synsetId, types):
        results = []
        _types = ""
        _revTypes = ""
        var8 = types
        var7 = len(types)
        for var6 in range(0, var7 - 1):
            type = var8[var6]
            _types += "'" + SynsetService.RelationValue(type) + "',"
            _revTypes += "'" + SynsetService.RelationValue(SynsetService.ReverseRelationType(type)) + "',"
        _types += "'not_type'"
        _revTypes += "'not_type'"
        sql = "SELECT id, type, synsetWords1, synsetWords2, synset, synset2, reverse_type FROM synset_relation WHERE (synset = " + str(
            synsetId) + " AND type in (" + _types + ")) OR (synset2 = " + str(
            synsetId) + " AND type in (" + _revTypes + "))" + " ORDER BY synset"
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SynsetRelation(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        resultsArr = []
        for i in range(0, len(results)):
            temp = results[i]
            if temp.synsetId1 != synsetId:
                type = temp.type
                synsetId2 = temp.synsetId2
                synsetId1 = temp.synsetId1
                synsetWords2 = temp.synsetWords2
                synsetWords1 = temp.synsetWords1
                reverseType = temp.reverseType
                temp.reverseType = type
                temp.synsetId1 = synsetId2
                temp.synsetId2 = synsetId1
                temp.synsetWords1 = synsetWords2
                temp.synsetWords2 = synsetWords1
                temp.type = reverseType
            resultsArr.append(temp)
        return results

    @staticmethod
    def getWordNetSynsets(synsetId):
        results = []
        sql = "SELECT id, wnPos, wnOffset, example, gloss, synset, type FROM wordnetsynset WHERE synset=" + str(
            synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(WordNetSynset(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return results

    def getSynsetExamples(synsetId):
        results = []
        sql = "SELECT gloss_and_example.id, content, lexicon.title FROM gloss_and_example INNER JOIN lexicon ON gloss_and_example.lexicon=lexicon.id WHERE type='EXAMPLE' and synset=" + str(
            synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SynsetExample(row[0], row[1], row[2]))
        return results

    @staticmethod
    def getSynsetGlosses(synsetId):
        results = []
        sql = "SELECT gloss_and_example.id, content, lexicon.title FROM gloss_and_example INNER JOIN lexicon ON gloss_and_example.lexicon=lexicon.id WHERE type='GLOSS' and synset=" + str(
            synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SynsetGloss(row[0], row[1], row[2]))
        return results

    @staticmethod
    def NormalValue(Value):
        NormalValue = Value.replace("ی", "ي")
        NormalValue = NormalValue.replace("ى", "ي")
        NormalValue = NormalValue.replace("ك", "ک")
        NormalValue = NormalValue.replace("'", "")
        NormalValue = NormalValue.replace("\"", "")
        NormalValue = NormalValue.replace(" ", "")
        NormalValue = NormalValue.replace("\u200c", "")
        NormalValue = NormalValue.replace("\u200c\u200cء", "")
        NormalValue = NormalValue.replace("\u200c\u200cٔ", "")
        NormalValue = NormalValue.replace("\u200c\u200cؤ", "و")
        NormalValue = NormalValue.replace("\u200c\u200cئ", "ي")
        NormalValue = NormalValue.replace("آ", "ا")
        NormalValue = NormalValue.replace("\u200c\u200cأ", "ا")
        NormalValue = NormalValue.replace("إ", "ا")
        NormalValue = NormalValue.replace("ۀ", "ه")
        NormalValue = NormalValue.replace("ة", "ه")
        NormalValue = NormalValue.replace("َ", "")
        NormalValue = NormalValue.replace("ُ", "")
        NormalValue = NormalValue.replace("ِ", "")
        NormalValue = NormalValue.replace("ً", "")
        NormalValue = NormalValue.replace("ٌ", "")
        NormalValue = NormalValue.replace("ٍ", "")
        NormalValue = NormalValue.replace("ّ", "")
        NormalValue = NormalValue.replace("ْ", "")
        NormalValue = NormalValue.replace("ِّ", "")
        NormalValue = NormalValue.replace("ٍّ", "")
        NormalValue = NormalValue.replace("َّ", "")
        NormalValue = NormalValue.replace("ًّ", "")
        NormalValue = NormalValue.replace("ُّ", "")
        NormalValue = NormalValue.replace("ٌّ", "")
        NormalValue = NormalValue.replace("u200D", "%")
        NormalValue = NormalValue.replace("ء", "")
        NormalValue = NormalValue.replace("أ", "ا")
        NormalValue = NormalValue.replace("ئ", "ي")
        return NormalValue

    @staticmethod
    def SecureValue(Value):
        if Value is None:
            return ""
        else:
            Value = Value.replace("\u0000", "")
            Value = Value.replace("'", "")
            Value = Value.replace("\"", "")
            Value = Value.replace("\b", "")
            Value = Value.replace("\n", "")
            Value = Value.replace("\r", "")
            Value = Value.replace("\t", "")
            Value = Value.replace("\\", "")
            Value = Value.replace("/", "")
            Value = Value.replace("%", "")
            Value = Value.replace("_", "")
            Value = Value.replace("ـ", "")
            Value = Value.replace("!", "")
            Value = Value.replace("", "")
            Value = Value.replace("?", "")
            Value = Value.replace("=", "")
            Value = Value.replace("<", "")
            Value = Value.replace(">", "")
            Value = Value.replace("&", "")
            Value = Value.replace("#", "")
            Value = Value.replace("@", "")
            Value = Value.replace("$", "")
            Value = Value.replace("^", "")
            Value = Value.replace("*", "")
            Value = Value.replace("+", "")
            return Value

    @staticmethod
    def RelationValue(type):
        if type.__str.toString() != "Related_to" and type.toString() != "Has-Unit" and type.toString().substring(
                3) != "Is_":
            if type.toString() == "Has_Salient_defining_feature":
                return "Has-Salient defining feature"
            else:
                return type.toString().replace("_", " ")
        else:
            return type.toString().replace("_", "-")

    @staticmethod
    def ReverseRelationType(type):
        if SynsetRelationType.Agent == type:
            return SynsetRelationType.Is_Agent_of
        elif SynsetRelationType.Is_Agent_of == type:
            return SynsetRelationType.Agent
        elif SynsetRelationType.Hypernym == type:
            return SynsetRelationType.Hyponym
        elif SynsetRelationType.Hyponym == type:
            return SynsetRelationType.Hypernym
        elif SynsetRelationType.Instance_hyponym == type:
            return SynsetRelationType.Instance_hypernym
        elif SynsetRelationType.Instance_hypernym == type:
            return SynsetRelationType.Instance_hyponym
        elif SynsetRelationType.Part_holonym == type:
            return SynsetRelationType.Part_meronym
        elif SynsetRelationType.Part_meronym == type:
            return SynsetRelationType.Part_holonym
        elif SynsetRelationType.Member_holonym == type:
            return SynsetRelationType.Member_meronym
        elif SynsetRelationType.Member_meronym == type:
            return SynsetRelationType.Member_holonym
        elif SynsetRelationType.Substance_holonym == type:
            return SynsetRelationType.Substance_meronym
        elif SynsetRelationType.Substance_meronym == type:
            return SynsetRelationType.Substance_holonym
        elif SynsetRelationType.Portion_holonym == type:
            return SynsetRelationType.Portion_meronym
        elif SynsetRelationType.Portion_meronym == type:
            return SynsetRelationType.Portion_holonym
        elif SynsetRelationType.Domain == type:
            return SynsetRelationType.Is_Domain_of
        elif SynsetRelationType.Is_Domain_of == type:
            return SynsetRelationType.Domain
        elif SynsetRelationType.Cause == type:
            return SynsetRelationType.Is_Caused_by
        elif SynsetRelationType.Is_Caused_by == type:
            return SynsetRelationType.Cause
        elif SynsetRelationType.Is_Instrument_of == type:
            return SynsetRelationType.Instrument
        elif SynsetRelationType.Instrument == type:
            return SynsetRelationType.Is_Instrument_of
        elif SynsetRelationType.Is_Entailed_by == type:
            return SynsetRelationType.Entailment
        elif SynsetRelationType.Entailment == type:
            return SynsetRelationType.Is_Entailed_by
        elif SynsetRelationType.Location == type:
            return SynsetRelationType.Is_Location_of
        elif SynsetRelationType.Is_Location_of == type:
            return SynsetRelationType.Location
        elif SynsetRelationType.Has_Salient_defining_feature == type:
            return SynsetRelationType.Salient_defining_feature
        elif SynsetRelationType.Salient_defining_feature == type:
            return SynsetRelationType.Has_Salient_defining_feature
        elif SynsetRelationType.Is_Attribute_of == type:
            return SynsetRelationType.Attribute
        elif SynsetRelationType.Attribute == type:
            return SynsetRelationType.Is_Attribute_of
        elif SynsetRelationType.Unit == type:
            return SynsetRelationType.Has_Unit
        elif SynsetRelationType.Has_Unit == type:
            return SynsetRelationType.Unit
        elif SynsetRelationType.Is_Patient_of == type:
            return SynsetRelationType.Patient
        else:
            if SynsetRelationType.Patient == type:
                return SynsetRelationType.Is_Patient_of
            else:
                return type


class SenseService:
    @staticmethod
    def getSensesByWord(searchStyle, searchKeyword):
        results = []
        sql = "SELECT sense.id, seqId, word.pos, word.defaultValue, word.id as wordId, word.avaInfo, vtansivity, vactivity, vtype, synset, vpastStem, vpresentStem, category, goupOrMokassar, esmeZamir, adad, adverb_type_1, adverb_type_2, adj_pishin_vijegi, adj_type, noe_khas, nounType, adj_type_sademorakkab, vIssababi, vIsIdiom, vGozaraType, kootah_nevesht, mohavere FROM sense INNER JOIN word ON sense.word = word.id WHERE sense.id IN (SELECT sense.id FROM word INNER JOIN sense ON sense.word = word.id LEFT OUTER JOIN value ON value.word = word.id WHERE word.search_value @SearchStyle '@SearchValue' OR value.search_value @SearchStyle '@SearchValue') OR sense.id IN (SELECT sense.id FROM sense INNER JOIN sense_relation ON sense.id = sense_relation.sense INNER JOIN sense AS sense_2 ON sense_2.id = sense_relation.sense2 INNER JOIN word ON sense_2.word = word.id WHERE sense_relation.type =  'Refer-to' AND word.search_value LIKE  '@SearchValue') OR sense.id IN (SELECT sense_2.id FROM sense INNER JOIN sense_relation ON sense.id = sense_relation.sense INNER JOIN sense AS sense_2 ON sense_2.id = sense_relation.sense2 INNER JOIN word ON sense.word = word.id WHERE sense_relation.type =  'Refer-to' AND word.search_value LIKE  '@SearchValue') "
        searchKeyword = SenseService.SecureValue(SenseService.NormalValue(searchKeyword))
        if searchStyle == "LIKE" or searchStyle == "START" or searchStyle == "END":
            sql = sql.replace("@SearchStyle", "LIKE")
            if searchStyle == "LIKE":
                searchKeyword = "%" + searchKeyword + "%"
            if searchStyle == "START":
                searchKeyword += "%"
            if searchStyle == "END":
                searchKeyword = "%" + searchKeyword
        if searchStyle == "EXACT":
            sql = sql.replace("@SearchStyle", "=")
        sql = sql.replace("@SearchValue", searchKeyword)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(
                Sense(row[0], row[1], row[2], row[3], row[4], row[5], SenseService.getVtansivity(row[6]),
                      SenseService.getVactivity(row[7]),
                      SenseService.getVtype(row[8]), SenseService.getNormalValue(row[9]),
                      SenseService.getNormalValue(row[10]),
                      SenseService.getNormalValue(row[11]), SenseService.getCategory(row[12]),
                      SenseService.getGoupOrMokassar(row[13]),
                      SenseService.getEsmeZamir(row[14]),
                      SenseService.getAdad(row[15]), SenseService.getAdverbType1(row[16]),
                      SenseService.getAdverbType2(row[17]),
                      SenseService.getAdjPishinVijegi(row[18]),
                      SenseService.getAdjType(row[19]), SenseService.getNoeKhas(row[20]),
                      SenseService.getNounType(row[21]),
                      SenseService.getAdjTypeSademorakkab(row[22]), row[23], row[24],
                      SenseService.getVGozaraType(row[25]), row[26], row[27]))
        return results

    @staticmethod
    def getSensesBySynset(synsetId):
        results = []
        sql = "SELECT sense.id, seqId, word.pos, word.defaultValue, word.id as wordId, word.avaInfo, vtansivity, vactivity, vtype, synset, vpastStem, vpresentStem, category, goupOrMokassar, esmeZamir, adad, adverb_type_1, adverb_type_2, adj_pishin_vijegi, adj_type, noe_khas, nounType, adj_type_sademorakkab, vIssababi, vIsIdiom, vGozaraType, kootah_nevesht, mohavere FROM sense INNER JOIN word ON sense.word = word.id WHERE sense.synset = " + str(
            synsetId)
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(
                Sense(row[0], row[1], row[2], row[3], row[4], row[5], SenseService.getVtansivity(row[6]),
                      SenseService.getVactivity(row[7]),
                      SenseService.getVtype(row[8]), SenseService.getNormalValue(row[9]),
                      SenseService.getNormalValue(row[10]),
                      SenseService.getNormalValue(row[11]), SenseService.getCategory(row[12]),
                      SenseService.getGoupOrMokassar(row[13]),
                      SenseService.getEsmeZamir(row[14]),
                      SenseService.getAdad(row[15]), SenseService.getAdverbType1(row[16]),
                      SenseService.getAdverbType2(row[17]),
                      SenseService.getAdjPishinVijegi(row[18]),
                      SenseService.getAdjType(row[19]), SenseService.getNoeKhas(row[20]),
                      SenseService.getNounType(row[21]),
                      SenseService.getAdjTypeSademorakkab(row[22]), row[23], row[24],
                      SenseService.getVGozaraType(row[25]), row[26], row[27]))
        return results

    @staticmethod
    def getSenseById(senseId):
        sql = "SELECT  sense.id, seqId, word.pos, word.defaultValue, word.id as wordId, word.avaInfo, vtansivity, vactivity, vtype, synset, vpastStem, vpresentStem, category, goupOrMokassar, esmeZamir, adad, adverb_type_1, adverb_type_2, adj_pishin_vijegi, adj_type, noe_khas, nounType, adj_type_sademorakkab, vIssababi, vIsIdiom, vGozaraType, kootah_nevesht, mohavere FROM sense INNER JOIN word ON sense.word = word.id WHERE sense.id = " + senseId
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            result = Sense(row[0], row[1], row[2], row[3], row[4], row[5], SenseService.getVtansivity(row[6]),
                           SenseService.getVactivity(row[7]),
                           SenseService.getVtype(row[8]), SenseService.getNormalValue(row[9]),
                           SenseService.getNormalValue(row[10]),
                           SenseService.getNormalValue(row[11]), SenseService.getCategory(row[12]),
                           SenseService.getGoupOrMokassar(row[13]),
                           SenseService.getEsmeZamir(row[14]),
                           SenseService.getAdad(row[15]), SenseService.getAdverbType1(row[16]),
                           SenseService.getAdverbType2(row[17]),
                           SenseService.getAdjPishinVijegi(row[18]),
                           SenseService.getAdjType(row[19]), SenseService.getNoeKhas(row[20]),
                           SenseService.getNounType(row[21]),
                           SenseService.getAdjTypeSademorakkab(row[22]), row[23], row[24],
                           SenseService.getVGozaraType(row[25]), row[26], row[27])
        return result

    @staticmethod
    def getAllSenses():
        results = []
        sql = "SELECT  sense.id, seqId, word.pos, word.defaultValue, word.id as wordId, word.avaInfo, vtansivity, vactivity, vtype, synset, vpastStem, vpresentStem, category, goupOrMokassar, esmeZamir, adad, adverb_type_1, adverb_type_2, adj_pishin_vijegi, adj_type, noe_khas, nounType, adj_type_sademorakkab, vIssababi, vIsIdiom, vGozaraType, kootah_nevesht, mohavere FROM sense INNER JOIN word ON sense.word = word.id"
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(
                Sense(row[0], row[1], row[2], row[3], row[4], row[5], SenseService.getVtansivity(row[6]),
                      SenseService.getVactivity(row[7]),
                      SenseService.getVtype(row[8]), SenseService.getNormalValue(row[9]),
                      SenseService.getNormalValue(row[10]),
                      SenseService.getNormalValue(row[11]), SenseService.getCategory(row[12]),
                      SenseService.getGoupOrMokassar(row[13]),
                      SenseService.getEsmeZamir(row[14]),
                      SenseService.getAdad(row[15]), SenseService.getAdverbType1(row[16]),
                      SenseService.getAdverbType2(row[17]),
                      SenseService.getAdjPishinVijegi(row[18]),
                      SenseService.getAdjType(row[19]), SenseService.getNoeKhas(row[20]),
                      SenseService.getNounType(row[21]),
                      SenseService.getAdjTypeSademorakkab(row[22]), row[23], row[24],
                      SenseService.getVGozaraType(row[25]), row[26], row[27]))
        return results

    @staticmethod
    def getSenseRelationsById(senseId):
        results = []
        sql = "SELECT id, sense, sense2, senseWord1, senseWord2, type FROM sense_relation WHERE sense = " + senseId + " OR sense2 = " + senseId
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SenseRelation(row[0], row[1], row[2], row[3], row[4], row[5]))
        resultsArr = []
        for i in range(0, len(results)):
            temp = results[i]
            if temp.senseId1 != senseId:
                type = temp.type
                senseId2 = temp.senseId2
                senseId1 = temp.senseId1
                senseWord2 = temp.senseWord2
                senseWord1 = temp.senseWord1
                temp.type = SenseService.ReverseSRelationType(type)
                temp.senseId1 = senseId2
                temp.senseId2 = senseId1
                temp.senseWord1 = senseWord2
                temp.senseWord2 = senseWord1
            resultsArr.append(temp)
        return resultsArr

    @staticmethod
    def getSenseRelationsByType(senseId, types):
        results = []
        _types = ""
        _revTypes = ""
        var8 = types
        var7 = types.length
        for var6 in range(0, var7 - 1):
            type = var8[var6]
            _types += "'" + SenseService.RelationValue(type) + "',"
            _revTypes += "'" + SenseService.RelationValue(SenseService.ReverseRelationType(type)) + "',"
        _types += "'not_type'"
        _revTypes += "'not_type'"
        sql = "SELECT id, sense, sense2, senseWord1, senseWord2, type FROM sense_relation WHERE (sense = " + senseId + " AND type in (" + _types + ")) OR (sense2 = " + senseId + " AND type in (" + _revTypes + "))" + " ORDER BY sense"
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SenseRelation(row[0], row[1], row[2], row[3], row[4], row[5]))
        resultsArr = []
        for i in range(0, len(results)):
            temp = results[i]
            if temp.senseId1 != senseId:
                type = temp.type
                senseId2 = temp.senseId2
                senseId1 = temp.senseId1
                senseWord2 = temp.senseWord2
                senseWord1 = temp.senseWord1
                temp.type = SenseService.ReverseSRelationType(type)
                temp.senseId1 = senseId2
                temp.senseId2 = senseId1
                temp.senseWord1 = senseWord2
                temp.senseWord2 = senseWord1
            resultsArr.append(temp)
        return resultsArr

    @staticmethod
    def getPhoneticFormsByWord(wordId):
        results = []
        sql = "SELECT id, value FROM speech WHERE word = " + wordId
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SenseRelation(row[0], row[1]))
        return results

    @staticmethod
    def getWrittenFormsByWord(wordId):
        results = []
        sql = "SELECT id, value FROM value WHERE word = " + wordId
        connection = SqlLiteDbUtility().getConnection()
        cursor = connection.execute(sql)
        for row in cursor:
            results.append(SenseRelation(row[0], row[1]))
        return results

    @staticmethod
    def NormalValue(Value):
        NormalValue = Value.replace("ی", "ي")
        NormalValue = NormalValue.replace("ى", "ي")
        NormalValue = NormalValue.replace("ك", "ک")
        NormalValue = NormalValue.replace("'", "")
        NormalValue = NormalValue.replace("\"", "")
        NormalValue = NormalValue.replace(" ", "")
        NormalValue = NormalValue.replace("\u200c", "")
        NormalValue = NormalValue.replace("\u200c\u200cء", "")
        NormalValue = NormalValue.replace("\u200c\u200cٔ", "")
        NormalValue = NormalValue.replace("\u200c\u200cؤ", "و")
        NormalValue = NormalValue.replace("\u200c\u200cئ", "ي")
        NormalValue = NormalValue.replace("آ", "ا")
        NormalValue = NormalValue.replace("\u200c\u200cأ", "ا")
        NormalValue = NormalValue.replace("إ", "ا")
        NormalValue = NormalValue.replace("ۀ", "ه")
        NormalValue = NormalValue.replace("ة", "ه")
        NormalValue = NormalValue.replace("َ", "")
        NormalValue = NormalValue.replace("ُ", "")
        NormalValue = NormalValue.replace("ِ", "")
        NormalValue = NormalValue.replace("ً", "")
        NormalValue = NormalValue.replace("ٌ", "")
        NormalValue = NormalValue.replace("ٍ", "")
        NormalValue = NormalValue.replace("ّ", "")
        NormalValue = NormalValue.replace("ْ", "")
        NormalValue = NormalValue.replace("ِّ", "")
        NormalValue = NormalValue.replace("ٍّ", "")
        NormalValue = NormalValue.replace("َّ", "")
        NormalValue = NormalValue.replace("ًّ", "")
        NormalValue = NormalValue.replace("ُّ", "")
        NormalValue = NormalValue.replace("ٌّ", "")
        NormalValue = NormalValue.replace("u200D", "%")
        NormalValue = NormalValue.replace("ء", "")
        NormalValue = NormalValue.replace("أ", "ا")
        NormalValue = NormalValue.replace("ئ", "ي")
        return NormalValue

    @staticmethod
    def SecureValue(Value):
        if Value is None:
            return ""
        else:
            Value = Value.replace("\u0000", "")
            Value = Value.replace("'", "")
            Value = Value.replace("\"", "")
            Value = Value.replace("\b", "")
            Value = Value.replace("\n", "")
            Value = Value.replace("\r", "")
            Value = Value.replace("\t", "")
            Value = Value.replace("\\", "")
            Value = Value.replace("/", "")
            Value = Value.replace("%", "")
            Value = Value.replace("_", "")
            Value = Value.replace("ـ", "")
            Value = Value.replace("!", "")
            Value = Value.replace("", "")
            Value = Value.replace("?", "")
            Value = Value.replace("=", "")
            Value = Value.replace("<", "")
            Value = Value.replace(">", "")
            Value = Value.replace("&", "")
            Value = Value.replace("#", "")
            Value = Value.replace("@", "")
            Value = Value.replace("$", "")
            Value = Value.replace("^", "")
            Value = Value.replace("*", "")
            Value = Value.replace("+", "")
            return Value

    @staticmethod
    def getVtansivity(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1724158427:
                if value == "transitive":
                    return "Transitive"
            elif hash(value) == 841936170:
                if value == "inTransitive":
                    return "Intransitive"
            elif hash(value) == 1845861045:
                if value == "dovajhi":
                    return "Causative/Anticausative"
            return value
        else:
            return ""

    @staticmethod
    def getVactivity(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1422950650:
                if value == "active":
                    return "Active"
            elif hash(value) == -792039641:
                if value == "passive":
                    return "Passive"
            return value
        else:
            return ""

    @staticmethod
    def getVtype(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1431524879:
                if value == "simpleVerb":
                    return "Simple"
            elif hash(value) == -1054772775:
                if value == "pishvandiVerb":
                    return "Phrasal"
            elif hash(value) == -570810619:
                if value == "auxiliaryVerb":
                    return "Auxiliary"
            elif hash(value) == 530219749:
                if value == "copulaVerb":
                    return "Copula"
            elif hash(value) == 1665965418:
                if value == "compoundVerb":
                    return "Complex"
            return value
        else:
            return ""

    @staticmethod
    def getCategory(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -49458414:
                if value == "category_masdari":
                    return "Infinitival"
            elif hash(value) == 318357937:
                if value == "category_esmZamir":
                    return "Pronoun"
            elif hash(value) == 338298407:
                if value == "category_adad":
                    return "Numeral"
            elif hash(value) == 338599184:
                if value == "category_khAs":
                    return "Specific"
            elif hash(value) == 1537779501:
                if value == "category_Am":
                    return "General"
            return value
        else:
            return ""

    @staticmethod
    def getGoupOrMokassar(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -826418989:
                if value == "am_khas_esmejam":
                    return "MassNoun"
            elif hash(value) == 134174425:
                if value == "am_khas_jam":
                    return "Regular"
            elif hash(value) == 1892681254:
                if value == "am_khas_mokassar":
                    return "Irregular"
            return value
        else:
            return ""

    @staticmethod
    def getEsmeZamir(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -969140441:
                if value == "gheir_moshakhas":
                    return "Indefinite"
            elif hash(value) == 534797624:
                if value == "motaghabel":
                    return "Reciprocal"
            elif hash(value) == 714990811:
                if value == "noun_type_morakab":
                    return ""
            elif hash(value) == 1224364290:
                if value == "moakkad":
                    return "Emphatic"
            return value
        else:
            return ""

    @staticmethod
    def getAdad(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1537886559:
                if value == "tartibi":
                    return "Ordinal"
            elif hash(value) == 3003695:
                if value == "asli":
                    return "Cardinal"
            return value
        else:
            return ""

    @staticmethod
    def getAdverbType1(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1609563487:
                if value == "moshtagh_morakab":
                    return "DerivationalCompound"
            elif hash(value) == -221942702:
                if value == "morakkab":
                    return "Compound"
            elif hash(value) == -186590203:
                if value == "moshtagh":
                    return "Derivative"
            elif hash(value) == 109191060:
                if value == "saade":
                    return "Simple"
            return value
        else:
            return ""

    @staticmethod
    def getNormalValue(value):
        if value is not None and value != "" and value != "Nothing":
            return value
        else:
            return ""

    @staticmethod
    def getAdverbType2(value):
        if value is not None and value != "" and value != "Nothing":
            res = " "
            if value[0] == '1':
                res += "AdjectiveModifying,"
            else:
                res += value[0] + ","
            if value[1] == '1':
                res += "AdverbModifying,"
            else:
                res += value[1] + ","
            if value[2] == '1':
                res += "VerbModifying,"
            else:
                res += value[2] + ","
            if value[3] == '1':
                res += "SentenceModifying,"
            else:
                res += value[3] + ","
            return res[:len(res) - 1]
        else:
            return ""

    @staticmethod
    def getAdjPishinVijegi(value):
        if value is not None and value != "" and value != "Nothing" and value != "No":
            if hash(value) == -282395544:
                if value == "Yes_taajobi":
                    return "Exclamatory"
            elif hash(value) == 770492981:
                if value == "Yes_Nothing":
                    return "Simple"
            elif hash(value) == 1795033874:
                if value == "Yes_eshare":
                    return "Demonstrative"
            elif hash(value) == 2020200460:
                if value == "Yes_mobham":
                    return "Indefinite"
            return value
        else:
            return ""

    @staticmethod
    def getAdjType(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1735880873:
                if value == "bartarin":
                    return "Superlative"
            elif hash(value) == -1396218190:
                if value == "bartar":
                    return "Comparative"
            elif hash(value) == 1241931560:
                if value == "motlagh":
                    return "Absolute"
            return value
        else:
            return ""

    @staticmethod
    def getNoeKhas(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -533828350:
                if value == "noe_khas_ensan":
                    return "Human"
            elif hash(value) == -526835153:
                if value == "noe_khas_makan":
                    return "Place"
            elif hash(value) == -514827458:
                if value == "noe_khas_zaman":
                    return "Time"
            elif hash(value) == 708964732:
                if value == "noe_khas_heyvan":
                    return "Animal"
            return value
        else:
            return ""

    def getAdjTypeSademorakkab(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1398986386:
                if value == "adj_type_morakab":
                    return "Compound"
            elif hash(value) == -383542830:
                if value == "adj_type_moshtagh":
                    return "Derivative"
            elif hash(value) == -264504089:
                if value == "adj_type_saade":
                    return "Simple"
            elif hash(value) == 1930601326:
                if value == "adj_type_moshtagh_morakab":
                    return "DerivatinalCompound"
            return value
        else:
            return ""

    @staticmethod
    def getVGozaraType(value):
        if value is not None and value != "" and value != "Nothing":
            res = " "
            if value[0] == '1':
                res += "WithComplement,"
            else:
                res += value[0] + ","
            if value[1] == '1':
                res += "WithObject,"
            else:
                res += value[1] + ","
            if value[2] == '1':
                res += "WithPredicate,"
            else:
                res += value[2] + ","
            return res[:len(res) - 1]
        else:
            return ""

    @staticmethod
    def getNounType(value):
        if value is not None and value != "" and value != "Nothing":
            if hash(value) == -1881033151:
                if value == "noun_type_ebarat":
                    return "Phrasal"
            elif hash(value) == -601968748:
                if value == "noun_type_saade":
                    return "Simple"
            elif hash(value) == 714990811:
                if value == "noun_type_morakab":
                    return "Compound"
            elif hash(value) == 725240837:
                if value == "noun_type_moshtagh":
                    return "Derivative"
            elif hash(value) == 1576628897:
                if value == "noun_type_moshtagh_morakab":
                    return "DerivatinalCompound"
            return value
        else:
            return ""

    @staticmethod
    def RelationValue(type):
        if type.__str__ == "Derivationally_related_form":
            return "Derivationally related form"
        else:
            return type.__str__.replace("_", "-")

    @staticmethod
    def ReverseRelationType(type):
        if SenseRelationType.Refer_to == type:
            return SenseRelationType.Is_Referred_by
        elif SenseRelationType.Is_Referred_by == type:
            return SenseRelationType.Refer_to
        elif SenseRelationType.Verbal_Part == type:
            return SenseRelationType.Is_Verbal_Part_of
        elif SenseRelationType.Is_Verbal_Part_of == type:
            return SenseRelationType.Verbal_Part
        elif SenseRelationType.Is_Non_Verbal_Part_of == type:
            return SenseRelationType.Non_Verbal_Part
        else:
            if SenseRelationType.Non_Verbal_Part == type:
                return SenseRelationType.Is_Non_Verbal_Part_of
            else:
                return type

    @staticmethod
    def ReverseSRelationType(type):
        if type == "Refer-to":
            return "Is-Referred-by"
        elif type == "Is-Referred-by":
            return "Refer-to"
        elif type == "Verbal-Part":
            return "Is-Verbal-Part-of"
        elif type == "Is-Verbal-Part-of":
            return "Verbal-Part"
        elif type == "Non-Verbal-Part":
            return "Is-Non-Verbal-Part-of"
        else:
            if type == "Is-Non-Verbal-Part-of":
                return "Non-Verbal-Part"
            else:
                return type


class Sense:

    def __init__(self, id, seqId, pos, defaultValue, wordId, defaultPhonetic, verbTransitivity, verbActivePassive,
                 verbType, synset, verbPastStem, verbPresentStem, nounCategory, nounPluralType, pronoun,
                 nounNumeralType, adverbType1, adverbType2, preNounAdjectiveType, adjectiveType2, nounSpecifityType,
                 nounType, adjectiveType1, isCausative, isIdiomatic, transitiveType, isAbbreviation, isColloquial):
        self.id = id
        self.isColloquial = isColloquial
        self.isAbbreviation = isAbbreviation
        self.transitiveType = transitiveType
        self.isIdiomatic = isIdiomatic
        self.isCausative = isCausative
        self.adjectiveType1 = adjectiveType1
        self.nounType = nounType
        self.nounSpecifityType = nounSpecifityType
        self.adjectiveType2 = adjectiveType2
        self.preNounAdjectiveType = preNounAdjectiveType
        self.adverbType1 = adverbType1
        self.adverbType2 = adverbType2
        self.nounNumeralType = nounNumeralType
        self.pronoun = pronoun
        self.nounPluralType = nounPluralType
        self.nounCategory = nounCategory
        self.verbPastStem = verbPastStem
        self.verbPresentStem = verbPresentStem
        self.synset = synset
        self.verbType = verbType
        self.verbActivePassive = verbActivePassive
        self.verbTransitivity = verbTransitivity
        self.id = id
        self.seqId = seqId
        self.value = defaultValue
        self.word = Word(wordId, pos, defaultPhonetic, defaultValue)

    def getSynset(self):
        if self.synset is not None and self.synset != "":
            return SynsetService.getSynsetById(int(self.synset))

    def getSenseRelations(self):
        return SenseService.getSenseRelationsById(self.id)

    def getSenseRelations(self, relationType):
        return SenseService.getSenseRelationsByType(self.id, relationType)

    def getSenseRelations(self, relationTypes):
        return SenseService.getSenseRelationsByType(self.id, relationTypes)


class PhoneticForm:
    def __init__(self, id, value):
        self.id = id
        self.value = value


class WrittenForm:
    def __init__(self, id, value):
        self.id = id
        self.value = value


class SenseRelation:
    def __init__(self, id, senseId1, senseId2, senseWord1, senseWord2, type):
        self.id = id
        self.senseId1 = senseId1
        self.senseId2 = senseId2
        self.senseWord1 = senseWord1
        self.senseWord2 = senseWord2
        self.type = type

    def getSense1(self):
        return SenseService.getSenseById(self.senseId1)

    def getSense2(self):
        return SenseService.getSenseById(self.senseId2)


class SenseRelationType(enum.Enum):
    Antonym = 0
    Refer_to = 1
    Is_Referred_by = 2
    Is_Non_Verbal_Part_of = 3
    Non_Verbal_Part = 4
    Verbal_Part = 5
    Is_Verbal_Part_of = 6
    Co_Occurrence = 7
    Derivationally_related_form = 8


class Synset:
    def __init__(self, id, pos, semanticCategory, example, gloss, nofather, noMapping):
        self.id = id
        self.semanticCategory = semanticCategory
        self.example = example
        self.gloss = gloss
        self.nofather = nofather
        self.noMapping = noMapping
        self.pos = pos

    def getExamples(self):
        return SynsetService.getSynsetExamples(self.id)

    def getGlosses(self):
        return SynsetService.getSynsetGlosses(self.id)

    def getSenses(self):
        return SenseService.getSensesBySynset(self.id)

    def getWordNetSynsets(self):
        return SynsetService.getWordNetSynsets(self.id)

    def getSynsetRelation(self):
        return SynsetService.getSynsetRelationsById(self.id)

    def getSynsetRelations(self, relationType):
        return SynsetService.getSynsetRelationsByType(self.id, relationType)


class SynsetExample:
    def __init__(self, id, content, lexicon):
        self.id = id
        self.content = content
        self.lexicon = lexicon


class SynsetGloss:
    def __init__(self, id, content, lexicon):
        self.id = id
        self.content = content
        self.lexicon = lexicon


class SynsetRelation:
    def __init__(self, id, type, synsetWords1, synsetWords2, synsetId1, synsetId2, reverseType):
        self.id = id
        self.type = type
        self.synsetWords1 = synsetWords1
        self.synsetWords2 = synsetWords2
        self.synsetId1 = synsetId1
        self.synsetId2 = synsetId2
        self.reverseType = reverseType

    def getSynset1(self):
        return SynsetService.getSynsetById(self.synsetId1)

    def getSynset2(self):
        return SynsetService.getSynsetById(self.synsetId2)


class SynsetRelationType(enum.Enum):
    Hypernym = 0
    Hyponym = 1
    Instance_hypernym = 2
    Instance_hyponym = 3
    Part_holonym = 4
    Part_meronym = 5
    Member_holonym = 6
    Member_meronym = 7
    Substance_holonym = 8
    Substance_meronym = 9
    Portion_holonym = 10
    Portion_meronym = 11
    Domain = 12
    Is_Domain_of = 13
    Antonym = 14
    Is_Agent_of = 15
    Agent = 17
    Is_Caused_by = 18
    Cause = 19
    Is_Instrument_of = 20
    Instrument = 21
    Is_Entailed_by = 22
    Entailment = 23
    Location = 24
    Is_Location_of = 25
    Has_Salient_defining_feature = 26
    Salient_defining_feature = 27
    Is_Attribute_of = 28
    Attribute = 29
    Unit = 30
    Has_Unit = 31
    Related_to = 32
    Is_Patient_of = 33
    Patient = 34


class Word:
    def __init__(self, id, pos, defaultPhonetic, defaultValue):
        self.id = id
        self.defaultPhonetic = defaultPhonetic
        self.defaultValue = defaultValue
        self.pos = pos

    def getWrittenForms(self):
        return SenseService.getWrittenFormsByWord(self.id)

    def getPhoneticForms(self):
        return SenseService.getPhoneticFormsByWord(self.id)


class WordNetSynset:
    def __init__(self, id, wnPos, wnOffset, example, gloss, synset, type):
        self.id = id
        self.wnPos = wnPos
        self.wnOffset = wnOffset
        self.example = example
        self.gloss = gloss
        self.synset = synset
        self.type = type
