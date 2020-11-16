<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <div class="row">
            <div class="col-sm-2">
                <img>
                    <xsl:attribute name="src">http://openweathermap.org/img/wn/<xsl:value-of select="time/symbol/@var"/>@4x.png</xsl:attribute>
                </img>
            </div>
            <div class="col-sm-2">
                <br/>
                <h5 class="text-warning"> <i class="fas fa-temperature-high"></i> <b> <xsl:value-of select="time/temperature/@max"/>°C</b> </h5>
                <h1><xsl:value-of select="time/temperature/@value"/>°C</h1>
                <h5 class="text-info"> <i class="fas fa-temperature-low"></i> <b> <xsl:value-of select="time/temperature/@min"/>°C</b></h5>
            </div>
        </div>
        <table class="table">
            <tbody>
                <tr>
                    <th scope="row">Temperatura</th>
                    <td><xsl:value-of select="time/temperature/@value"/>°C (min:<xsl:value-of select="time/temperature/@min"/>°C - max: <xsl:value-of select="time/temperature/@max"/> °C )</td>
                </tr>
                <tr>
                    <th scope="row">Sensação Térmica</th>
                    <td><xsl:value-of select="time/feels_like/@value"/> °C</td>
                </tr>
                <tr>
                    <th scope="row">Precipitação</th>
                    <td><xsl:value-of select="time/precipitation/@probability"/> %</td>
                </tr>
                <tr>
                    <th scope="row">Humidade</th>
                    <td><xsl:value-of select="time/humidity/@value"/> %</td>
                </tr>
                <tr>
                    <th scope="row">Pressão</th>
                    <td><xsl:value-of select="time/pressure/@value"/> hPa</td>
                </tr>
                <tr>
                    <th scope="row">Velocidade Vento</th>
                    <td><xsl:value-of select="time/windSpeed/@mps"/> m/s -- <xsl:value-of select="time/windSpeed/@name"/></td>
                </tr>
                <tr>
                    <th scope="row">Direção Vento</th>
                    <td><xsl:value-of select="time/windDirection/@name"/></td>
                </tr>
                <tr>
                    <th scope="row">Nuvens</th>
                    <td><xsl:value-of select="time/clouds/@all"/> % -- <xsl:value-of select="time/clouds/@value"/></td>
                </tr>
                <tr>
                    <th scope="row">Visibilidade</th>
                    <td><xsl:value-of select="time/visibility/@value"/></td>
                </tr>
            </tbody>
        </table>
    </xsl:template>
</xsl:stylesheet>