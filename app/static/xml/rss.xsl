<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html"/>
    <xsl:template match="/">
        <xsl:for-each select="//item">
        <div class="card">
            <div class="card-header">
                <h3><xsl:value-of select="title"/></h3>
            </div>
            <div class="card-body" style="height: 120px; overflow: hidden;">
                <xsl:value-of select="description" disable-output-escaping="yes"/>
            </div>
            <div class="card-footer">
                <p>
                    <b>Publicada em: </b>
                    <xsl:value-of select="pubDate"/>
                </p>
                <a target="_blank">
                    <xsl:attribute name="href">
                        <xsl:value-of select="link"/>
                    </xsl:attribute>
                    Aceder à notícia completa.
                </a>
            </div>
        </div>
            <br/>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>