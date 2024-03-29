// We multiply this unit by the (value of a country - min) to get the
// decimal value to provide to the Chroma scale instance.
const getColorScaleUnit = (min, max) => {
  if (max === min) {
    // Handles the case where we only have one country in the data.
    return 1
  } else {
    return 1 / (max - min);
  }
}

const getMaxAndMinCountryDataValues = (countryData) => {
  let min, max;

  Object.keys(countryData).forEach((key) => {
    if (key === 'unknown') return;

    const value = countryData[key];

    if (value < min || min === undefined) min = value;
    if (value > max || max === undefined) max = value;
  });

  return { min, max };
};

export const getBaseCss = ({ defaultCountryFillColor, countryStrokeColor, countryStrokeWidth, xxxMaskStrokeWidth, xxxStrokeDashArray, legendHeaderBackgroundColor, legendContentBackgroundColor, legendFontColorHeader, legendFontColorContent, legendBorderRadius, legendBorderColor, legendBoxShadow }) => (
  `.vue-world-map .land{
    fill:${defaultCountryFillColor};
    stroke:${countryStrokeColor};
    stroke-width: ${countryStrokeWidth};
  }
  .vue-world-map .xxx-mask{
    stroke: #fff;
    stroke-width: ${xxxMaskStrokeWidth};
  }
  .vue-world-map .xxx{
    stroke:${countryStrokeColor};
    stroke-width: ${countryStrokeWidth};
    stroke-dasharray: ${xxxStrokeDashArray};
  }
  .vue-map-legend-header{
    background:${legendHeaderBackgroundColor}
  }
  .vue-map-legend .vue-map-legend-content{
    background:${legendContentBackgroundColor}
  }
  .vue-map-legend-content span{
    color:${legendFontColorContent}
  }
  .vue-map-legend-header span{
    color:${legendFontColorHeader}
  }
.vue-map-legend{
    border-color: ${legendBorderColor}!important;
    border-radius:${legendBorderRadius}px;
    box-shadow: ${legendBoxShadow ? '3px 4px #00000017' : 'none'};
  }
  `
);

const getScaleValue = (value, min, max, colorScaleUnit) => {
  value = Number(value)
  if (isNaN(value)) {
    // Handle cases for "No Data" value.
    return value
  }

  let scaleValue = colorScaleUnit;
  if (min !== max) {
    scaleValue = colorScaleUnit * (value - min);
  }
  return scaleValue;
}

export const getDynamicMapCss = (countryData, chromaScale, highColor, chromaScaleOn) => {
  const { min, max } = getMaxAndMinCountryDataValues(countryData);
  const colorScaleUnit = getColorScaleUnit(min, max);
  const css = [];
  Object.keys(countryData).forEach((key) => {
    if (key === 'unknown') return;

    const value = countryData[key];
    const scaleValue = getScaleValue(value, min, max, colorScaleUnit);
    const hex = chromaScale(scaleValue).hex();
    css.push(`.vue-world-map #${key} { fill: ${chromaScaleOn ? hex : highColor}; }`);
  });
  return css;
};

export const getCombinedCssString = (baseCss, dynamicCss) => {
  dynamicCss.push(baseCss);

  return dynamicCss.join(' ');
};