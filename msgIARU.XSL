<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">
	<!-- 
	style-sheet for presenting xml data in an Radiogram form
	Copyright 2009, QED Software
	Free for Amateur use
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

table.radiogram { 
	width: "95%"; 
	text-align: center; 
	border-style: solid; 
	border-width: 0;
	padding-left: 0; 
	padding-right: 0; 
	padding-top: 1px; 
	padding-bottom: 1px
	cellspacing: "0"
}

table.title { 
	width: "100%";
	text-align: center;
	border-width: 0;
	cellspacing: "0";
 }

td.heading {
	font-size: .6em;
	text-align: center;
}

td.cell {
	font-size: 1em;
	text-align: center;
}

td.cell2 {
	font-size: 1em;
	width: 50%;
	vertical-align:bottom;
}

td.cell3 {
	font-size: 1em;
	width: 40;
	vertical-align:bottom;
}

td.fruo {
	font-size: 1.5em;
	text-align: left;
	vertical-align:bottom;
}

</style>
    </head>
        <body>
            <div align="center">
				<table class="radiogram">
					<tr>
						<td>
							<table class="title">
                                <tr>
									<td>
										<font size="3">
											<b>FNRASEC</b>
										</font>
										<br/>
										<font size="6">
											<b>RADIOGRAM</b>
										</font>
										<br/>
										<font size="1">(IARU Standard Message) via Amateur Radio</font>
										<xsl:if test="message/exercise = 'Exercice'">
											<font color="#FF0000">
												<br/>
												<b>&#160; [ EXERCISE ] &#160;</b>
											</font>
										</xsl:if>
									</td>
								</tr>
							</table>
							<table width="100%" border="1" cellspacing="0">
								<tr>
									<td class="heading">NUMBER</td>
									<td class="heading">PRECEDENCE</td>
									<td class="heading">STATION OF ORIGIN</td>
									<td class="heading">COUNT</td>
									<td class="heading">PLACE OF ORIGIN</td>
									<td class="heading">TIME FILED</td>
									<td class="heading">DATE</td>
								</tr>
								<tr>
									<td class="cell">
										<xsl:value-of select="message/id"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/precedance"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/origin/station"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/check"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/origin/place"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/filed/time"/>&#160;</td>
									<td class="cell">
										<xsl:value-of select="message/filed/date"/>&#160;</td>
								</tr>
							</table>
							<p/>
							<br/>
							<table width="100%" border="0" cellspacing="0">
								<tr>
									<td class="cell3">FROM :</td>
									<td>
										<xsl:value-of select="message/from"/>&#160;
                                    </td>
								</tr>
								<tr>
									<td class="cell3">TO :</td>
									<td>
										<xsl:for-each select="message/to">
											<xsl:value-of select="."/>
                                            &#160;
										</xsl:for-each>
									</td>
								</tr>
							</table>
							<br/>
							<table width="100%" border="1" cellspacing="0">
								<tr>
									<td>
										<p>
										<xsl:for-each select="message/body/para">
                                            <xsl:call-template name="replace-leading-space">
                                                <xsl:with-param name="str" select="."/>
											</xsl:call-template>
											<br />
										</xsl:for-each>
										</p>
										<p>&#160;</p>
									</td>
								</tr>
							</table>
							<p>&#160;</p>
							<table width="100%" border="0" cellspacing="0">
								<tr>
									<td class="fruo">For radio operator use only</td>
									<td></td>
								</tr>
							</table>
														
							<table width="100%" border="1" cellspacing="0">
								<tr>
									<td width="heading" class="heading">RECEIVED FROM</td>
									<td class="heading">DATE</td>
									<td class="heading">TIME</td>
									<td width="100px"></td>
									<td class="heading">SENT TO</td>
									<td class="heading">DATE</td>
									<td class="heading">TIME</td>
								</tr>
								<tr>
									<td><xsl:value-of select="message/receivedfrom/name"/>&#160;</td>
									<td><xsl:value-of select="message/receivedfrom/date"/>&#160;</td>
									<td><xsl:value-of select="message/receivedfrom/time"/>&#160;</td>
									<td></td>	
									<td><xsl:value-of select="message/sentto/name"/>&#160;</td>
									<td><xsl:value-of select="message/sentto/date"/>&#160;</td>
									<td><xsl:value-of select="message/sentto/time"/>&#160;</td>
								</tr>
							</table>
							<p/>
						</td>
					</tr>
					<tr>
						<td>
							<table width="100%" border="0" cellspacing="0">
								<tr>
									<th align="right">
										<font size="2">Radiogram
                                            <br/>
                                            <xsl:value-of select="message/software"/>&#160;<xsl:value-of select="message/version"/>
										</font>
									</th>
								</tr>
							</table>
						</td>
					</tr>
				</table>
			</div>
		</body>
	</html>
</xsl:template>
</xsl:stylesheet>
