<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <table class="table">
            <tbody>
                <xsl:for-each select="//item">
                <tr>
                    <th scope="row">Title</th>
                    <td><xsl:value-of select="title"/>°</td>
                </tr>
                <tr>
                    <th scope="row">Link</th>
                    <td>
                        <a>
                            <xsl:attribute name="href">
                                <xsl:value-of select="link"/>
                            </xsl:attribute>
                        </a>
                    </td>
                </tr>
                <tr>
                    <th scope="row">Description</th>
                    <td><xsl:value-of select="description"/></td>
                </tr>
                </xsl:for-each>
            </tbody>
        </table>
    </xsl:template>
</xsl:stylesheet>