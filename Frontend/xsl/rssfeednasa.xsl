<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html"/>
<xsl:template match="/">
  <div class="rss">
  <h2>RSS Feeds</h2>
  <xsl:for-each select="Request/data/RSS-Feed">
  <div class="rss-item">
      <div class="rss-image">
        <xsl:if test="starts-with(title,'S')">
          <img class="rss-stg" src="https://www.nasa.gov/sites/default/files/files/s2g_itunes.jpg"></img>
        </xsl:if>
        <xsl:if test="starts-with(title, 'I')">
          <img class="rss-sr" src="https://www.spacestationexplorers.org/wp-content/uploads/2018/02/iss-above-logo-square.jpg"></img>
        </xsl:if>
      </div>
      <div class="rss-text text">
          <h4><xsl:value-of select="title"/></h4>
          <p><xsl:value-of select="summary"/></p>
      </div>
  </div>
  </xsl:for-each>
  
    <div class="rss-buttons">
        <a class="rss-prev" onclick="rssClick(-1)"><span>&#10094;</span></a>
        <a class="rss-next" onclick="rssClick(1)"><span>&#10095;</span></a>
    </div>
    </div>
</xsl:template>
</xsl:stylesheet>