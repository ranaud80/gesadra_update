<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet de présentation des messages TMD
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
    color: blue
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
    background-color: orange;
    color: blue;
}
td.lib {
	width: 25%;
}
td.zone {
	width: 25%;
    text-align: center;
}
td.val {
	width: 25%;
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
						<table class="title" id="1">
                            <tr>
								<th class="title">ASSOCIATION DEPARTEMENTALE DES RADIOAMATEURS</th>
                            </tr>
                            <tr>
                                <th class="title">AU SERVICE DE LA SECURITE CIVILE</th>
                            </tr>
                            <tr>
                                <td>
                                    <hr size="3" color="blue" />
                                    <hr size="3" color="orange" />
                                </td>
                            </tr>
                            <tr>
                                <td class="title">MESSAGE</td>
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
                                <th class="pgh" colspan="2">Transport de Matières Dangereuses</th>
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
                                    <hr size="3" color="orange" />
                                </td>
                            </tr>
                        </table>
                        <table class="pgh">
                            <tr>
                                <th colspan="2">Description du véhicule</th>
                            </tr>
                            <tr>
                                <td class="lib">Véhicule</td>
								<td><xsl:value-of select="msg/corps/ong1/veh"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Type</td>
								<td><xsl:value-of select="msg/corps/ong1/type"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Poids</td>
								<td><xsl:value-of select="msg/corps/ong1/pveh"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Capacité</td>
								<td><xsl:value-of select="msg/corps/ong1/capa"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Volume du Fret</td>
								<td><xsl:value-of select="msg/corps/ong1/vfret"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Poids du Fret</td>
								<td><xsl:value-of select="msg/corps/ong1/pfret"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Comp. calorifugés</td>
								<td><xsl:value-of select="msg/corps/ong1/compart"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Syst. réchauffage</td>
								<td><xsl:value-of select="msg/corps/ong1/rechauf"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Syst. refrigérant</td>
								<td><xsl:value-of select="msg/corps/ong1/refrig"/>&#160;</td>
                            </tr>
						</table>
                        <table class="pgh">
							<tr>
                                <th colspan="2">Conditionnement du Fret</th>
                            </tr>
                            <tr>
                                <td class="lib">Conditionnement</td>
								<td><xsl:value-of select="msg/corps/ong2/cond"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Nombre</td>
								<td><xsl:value-of select="msg/corps/ong2/nbcond"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Poids ou volume</td>
								<td><xsl:value-of select="msg/corps/ong2/poids"/>&#160;</td>
                            </tr>
                        </table>
                        <table align="center">
                            <th colspan="4">Détail des emballages</th>
                            <tr>
                                <td class="val">Ss-emballage</td>
                                <td class="val">Matière</td>
                                <td class="val">Quantité</td>
                                <td class="val">Poids ou Volume</td>
							</tr>    
							<xsl:for-each select="msg/corps/ong2/emb">
                                <tr>
                                    <td class="zone"><xsl:value-of select="./ssemb"/>&#160;</td>
                                    <td class="zone"><xsl:value-of select="./mat"/>&#160;</td>
                                    <td class="zone"><xsl:value-of select="./qte"/>&#160;</td>
                                    <td class="zone"><xsl:value-of select="./pov"/>&#160;</td>
                                </tr>    
                            </xsl:for-each>
                        </table>
                        <table class="pgh">
                            <th colspan="2">Identité du transporteur</th>
                            <tr>
                                <td class="lib">Nom</td>
								<td><xsl:value-of select="msg/corps/ong3/nom"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Tél/Fax</td>
								<td><xsl:value-of select="msg/corps/ong3/tel"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Adresse</td>
								<td><xsl:value-of select="msg/corps/ong3/adr"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Immat. Véhicule</td>
								<td><xsl:value-of select="msg/corps/ong3/immat"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Nationalité</td>
								<td><xsl:value-of select="msg/corps/ong3/nation"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Expéd. Fret</td>
								<td><xsl:value-of select="msg/corps/ong3/exped"/>&#160;</td>
                            </tr>
                            <tr>
                                <td class="lib">Destin. Fret</td>
								<td><xsl:value-of select="msg/corps/ong3/client"/>&#160;</td>
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
                                        Message TMD
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
