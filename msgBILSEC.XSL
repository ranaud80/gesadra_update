<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet de présentation des messages BILAN SECOURISTE
	-->

  <!-- Subroutine that replaces a leading space or tab -->
  <!-- with a hard (non-breaking) space -->
  <!-- Input: parameter "str", a string -->
  <!-- Returns: value of "str" w/ leading space replaced -->
<xsl:template name="replace-leading-space">
    <xsl:param name="str"/>
    <xsl:variable name="first" select="substring( $str, 1, 1 )"/>
    <xsl:choose>
        <xsl:when test="$first='&#x20;' or $first='&#x09;'">
            <xsl:value-of select="concat('&#160;', substring( $str, 2 ))"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$str"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>
  
<xsl:output method="html" version="1.0" encoding="ISO-8859-1" indent="yes"/>
<xsl:template match="/">

<html>
	<head>
		<style type="text/css">

table.msg { 
	width: 700px; 
    font-family: Arial, Helvetica, sans-serif;
    font-size: .8em;
    border-style: solid; 
	border-width: 1px;
}

table.title { 
	width: 100%;
    font-weight: bold;
	text-align: center;
 }

th.title {
    font-size: 1.2em;
    color: gray
}

td.title {
    font-size: 2em;
}

td.mode {
    color: red;
}

table.pgh {
    width: 100%;
    border-width: 0;
}
th.pgh {
    text-align: center;
    background-color: gray;
    color: black;
}
td.lib {
	width: 25%;
}
td.zone {
	width: 28%;
}
td.val {
	width: 8%;
    text-align: center;
}

        </style>
        <script language="Javascript">
            function imp1(){window.print();}
            function imp2(){
                var targetElement;
                targetElement = document.getElementById('1') ;
                targetElement.style.display = "none" ;
                targetElement = document.getElementById('2') ;
                targetElement.style.display = "none" ;
                window.print();
                }
        </script>
    </head>
    <body align="center" width="700px">
        <table class="msg">
            <tr>
                <td>
                    <table  cellspacing="0" class="title" id="1">
                        
						<tr>
						<th height="15" width="15"></th><th width="15" bgcolor="red"></th><th width="15"></th>
                            <th rowspan="3" class="title">CROIX-ROUGE FRANCAISE</th>
						<th width="15"></th><th width="15" bgcolor="red"></th><th width="15"></th>
                        </tr>
						<tr>
						<th width="15" height="15" bgcolor="red"></th><th width="15" bgcolor="red"></th><th width="15" bgcolor="red"></th>
						<th bgcolor="red"></th><th bgcolor="red"></th><th bgcolor="red"></th>
						</tr>
						<tr>
						<th height="15"></th><th bgcolor="red"></th><th></th>
						<th></th><th bgcolor="red"></th><th></th>
						</tr>
                        <tr>
                            <td colspan="7" >
                                <hr size="1" color="red" />
                                <hr size="1" color="red" />
                            </td>
                        </tr>
                        <tr>
                            <td colspan="7" class="title">MESSAGE</td>
                        </tr>
                        <tr>
                            <td class="mode">
                                <xsl:if test="msg/mode = 'Exercice'">- EXERCICE - EXERCICE - EXERCICE -</xsl:if>
                            </td>
                        </tr>
                    </table>
                    <br/>
                    <table class="pgh">
                        <tr>
                            <th class="pgh" colspan="2">Informations transmission</th>
                        </tr>    
                        <tr>
                            <td class="lib">Groupe Date/Heure</td>
                            <td><xsl:value-of select="msg/trans/gdh"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Emis par</td>
                            <td><xsl:value-of select="msg/trans/emis"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Reçu par</td>
                            <td><xsl:value-of select="msg/trans/recu"/>&#160;</td>
                        </tr>
                        <tr>
                            <td>Instructions particulières</td>
                            <td><xsl:value-of select="msg/trans/instr"/>&#160;</td>
                        </tr>
                    </table>
                    <br/>
                    <table class="pgh">
                        <tr>
                            <th class="pgh" colspan="2">Bilan Secouriste</th>
                        </tr>    
                        <tr>
                            <td class="lib">Origine</td>
                            <td><xsl:value-of select="msg/top/from"/>&#160;</td>
                        </tr>    
                        <tr>
                            <td class="lib">Dest. Action</td>
                            <td><xsl:value-of select="msg/top/to"/>&#160;</td>
                        </tr>    
                        <tr>
                            <td class="lib">Dest. Info</td>
                            <td><xsl:value-of select="msg/top/info"/>&#160;</td>
                        </tr>    
                        <tr>
                            <td class="lib">Urgence</td>
                            <td><xsl:value-of select="msg/top/urg"/>&#160;</td>
                        </tr>    
                        <tr>
                            <td colspan = "3">
                                <hr size="3" color="gray" />
                            </td>
                        </tr>
                    </table>
                    <table class="pgh">
                        <tr>
                            <th colspan="2">Identité de la Victime</th>
                        </tr>
                        <tr>
                            <td class="lib">Num Victime</td>
                            <td><xsl:value-of select="msg/corps/ong1/num"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Age</td>
                            <td><xsl:value-of select="msg/corps/ong1/age"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Sexe</td>
                            <td><xsl:value-of select="msg/corps/ong1/sexe"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Nom - Prénom</td>
                            <td><xsl:value-of select="msg/corps/ong1/nom"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Adresse</td>
                            <td><xsl:value-of select="msg/corps/ong1/adr"/>&#160;</td>
                        </tr>
                        <tr>
                            <th colspan="2">Nature de la detresse</th>
                        </tr>
                        <tr>
                            <td class="lib">Nature</td>
                            <td><xsl:value-of select="msg/corps/ong1/nat"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Détr. Vitale</td>
                            <td><xsl:value-of select="msg/corps/ong1/vital"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Tri PMA</td>
                            <td><xsl:value-of select="msg/corps/ong1/pma"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Circonstances</td>
                            <td>
                                <xsl:for-each select="msg/corps/ong1/circ">
                                    <xsl:value-of select="."/><br/>
                                </xsl:for-each>
                            </td>
                        </tr>    
                    </table>
                    <table class="pgh">
                        <tr>
                            <th colspan="2">Conscience</th>
                        </tr>
                        <tr>
                            <td class="lib">Victime</td>
                            <td>
                                <xsl:value-of select="msg/corps/ong2/consc/etat"/>&#160;
                                <xsl:for-each select="msg/corps/ong2/consc/item">
                                    <xsl:value-of select="."/>&#160;
                                </xsl:for-each>
                            </td>
                        </tr>
                        <tr>
                            <td class="lib">PCI</td>
                            <td><xsl:value-of select="msg/corps/ong2/consc/pci"/></td>
                        </tr>
                        <tr>
                            <th colspan="2">Ventilation</th>
                        </tr>
                        <tr>
                            <td class="lib">Fréquence</td>
                            <td>
                                <xsl:value-of select="msg/corps/ong2/ventil/freq"/>&#160;
                                <xsl:for-each select="mas/corps/ong2/ventil/item">
                                    <xsl:value-of select="."/>&#160;
                                </xsl:for-each>
                            </td>
                        </tr>
                        <tr>
                            <td class="lib">Saturation</td>
                            <td><xsl:value-of select="msg/corps/ong2/ventil/sat"/></td>
                        </tr>
                        <tr>
                            <th colspan="2">Circulation</th>
                        </tr>
                        <tr>
                            <td class="lib">Fréquence</td>
                            <td>
                                <xsl:value-of select="msg/corps/ong2/circul/freq"/>&#160;
                                <xsl:for-each select="mas/corps/ong2/circul/item">
                                    <xsl:value-of select="."/>&#160;
                                </xsl:for-each>
                            </td>
                        </tr>
                        <tr>
                            <td class="lib">Tension</td>
                            <td><xsl:value-of select="msg/corps/ong2/circul/tension"/></td>
                        </tr>
                        <tr>
                            <th colspan="2">Réflexes Pupillaires</th>
                        </tr>
                        <tr>
                            <td class="lib">Pup. Gauche</td>
                            <td>
                                <xsl:value-of select="msg/corps/ong2/pupil/gauche"/>&#160;
                                <xsl:if test="msg/corps/ong2/pupil/reacg = '1'">Réactive</xsl:if>
                            </td>
                        </tr>
                        <tr>
                            <td class="lib">Pup. Droite</td>
                            <td>
                                <xsl:value-of select="msg/corps/ong2/pupil/droite"/>&#160;
                                <xsl:if test="msg/corps/ong2/pupil/reacd = '1'">Réactive</xsl:if>
                            </td>
                        </tr>
                    </table>
                    <table class="les">
                        <th colspan="11">Lésions</th>
                        <tr>
                            <td>&#160;</td>
                            <td class="val">Hémorragie</td>
                            <td class="val">Déformation</td>
                            <td class="val">Douleur</td>
                            <td class="val">Plaie</td>
                            <td class="val">Brulure</td>
                            <td class="val">Motricité</td>
                            <td class="val">Sensibilité</td>
                            <td class="val">Chaleur</td>
                            <td class="val">Coloration</td>
                        </tr>    
                        <xsl:for-each select="msg/corps/ong3/lesion">
                            <tr>
                                <td class="zone"><xsl:value-of select="./zone"/>&#160;</td>
                                <xsl:for-each select="./val">
                                    <td class="val"><xsl:value-of select="."/>&#160;</td>
                                </xsl:for-each>
                            </tr>    
                        </xsl:for-each>
                    </table>
                    <table class="pgh">
                        <th colspan="2">Gestes et Soins</th>
                        <tr>
                            <td class="lib">Gestes effectués</td>
                            <td>
                                <xsl:for-each select="msg/corps/ong4/geste">
                                    <xsl:value-of select="."/><br/>
                                </xsl:for-each>
                            </td>
                        </tr>    
                        <tr>
                            <td class="lib">Soins effectués</td>
                            <td>
                                <xsl:for-each select="msg/corps/ong4/soin">
                                    <xsl:value-of select="."/><br/>
                                </xsl:for-each>
                            </td>
                        </tr>    
                        <tr>
                            <td class="lib">Prise en charge</td>
                            <td><xsl:value-of select="msg/corps/ong4/condi"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Evacuation</td>
                            <td><xsl:value-of select="msg/corps/ong4/evac"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Destination</td>
                            <td><xsl:value-of select="msg/corps/ong4/dest"/>&#160;</td>
                        </tr>
                    </table>
                    <br/>
                    <table class="pgh">
                        <tr>
                            <th class="pgh" colspan="2">Fin message</th>
                        </tr>    
                        <tr>
                            <td class="lib">GDH Dépôt</td>
                            <td><xsl:value-of select="msg/bot/gdh"/>&#160;</td>
                        </tr>
                        <tr>
                            <td class="lib">Demande A.R.</td>
                            <td><xsl:value-of select="msg/bot/ack"/>&#160;</td>
                        </tr>
                    </table>
                    <br/>
                    <table class="title" id="2">
                        <tr>
                            <td class="mode">
                                <xsl:if test="msg/mode = 'Exercice'">- EXERCICE - EXERCICE - EXERCICE -</xsl:if>
                            </td>
                        </tr>
                        <tr>
                            <td align="right">
                                <font size="1.5px">
                                    Message BilSec
                                    <br/>
                                    <xsl:value-of select="msg/soft"/>&#160;<xsl:value-of select="msg/vers"/>
                                </font>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        <div align="center"><input name="B1" onclick="imp1()" type="button" value="Imprimer Tout"/></div>
        <div align="center"><input name="B2" onclick="imp2()" type="button" value="Imprimer Message seul"/></div>
	</body>
</html>

</xsl:template>
</xsl:stylesheet>
