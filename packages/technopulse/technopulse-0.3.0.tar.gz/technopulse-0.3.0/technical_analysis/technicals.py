

class Recommendation:
    buy = "BUY"
    sell = "SELL"
    neutral = "NEUTRAL"


class Compute:
    def MA_CALCULATION(ma, close):
        """Compute Moving Average

        Args:
            ma (float): MA value
            close (float): Close value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (ma < close):
            return Recommendation.buy
        elif (ma > close):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def RSI_CALCULATION(rsi, rsi1):
        """Compute Relative Strength Index

        Args:
            rsi (float): RSI value
            rsi1 (float): RSI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (rsi < 30 and rsi1 < rsi):
            return Recommendation.buy
        elif (rsi > 70 and rsi1 > rsi):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Stoch_CALCULATION(k, d, k1, d1):
        """Compute Stochastic

        Args:
            k (float): Stoch.K value
            d (float): Stoch.D value
            k1 (float): Stoch.K[1] value
            d1 (float): Stoch.D[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (k < 20 and d < 20 and k > d and k1 < d1):
            return Recommendation.buy
        elif (k > 80 and d > 80 and k < d and k1 > d1):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def CCI20_CALCULATION(cci20, cci201):
        """Compute Commodity Channel Index 20

        Args:
            cci20 (float): CCI20 value
            cci201 ([type]): CCI20[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (cci20 < -100 and cci20 > cci201):
            return Recommendation.buy
        elif (cci20 > 100 and cci20 < cci201):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def ADX_CALCULATION(adx, adxpdi, adxndi, adxpdi1, adxndi1):
        """Compute Average Directional Index

        Args:
            adx (float): ADX value
            adxpdi (float): ADX+DI value
            adxndi (float): ADX-DI value
            adxpdi1 (float): ADX+DI[1] value
            adxndi1 (float): ADX-DI[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (adx > 20 and adxpdi1 < adxndi1 and adxpdi > adxndi):
            return Recommendation.buy
        elif (adx > 20 and adxpdi1 > adxndi1 and adxpdi < adxndi):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def AO_CALCULATION(ao, ao1, ao2):
        """Compute Awesome Oscillator

        Args:
            ao (float): AO value
            ao1 (float): AO[1] value
            ao2 (float): AO[2] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (ao > 0 and ao1 < 0) or (ao > 0 and ao1 > 0 and ao > ao1 and ao2 > ao1):
            return Recommendation.buy
        elif (ao < 0 and ao1 > 0) or (ao < 0 and ao1 < 0 and ao < ao1 and ao2 < ao1):
            return Recommendation.sell
        else:
            return Recommendation.neutral

    def Mom_CALCULATION(mom, mom1):
        """Compute Momentum

        Args:
            mom (float): Mom value
            mom1 (float): Mom[1] value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (mom < mom1):
            return Recommendation.sell
        elif (mom > mom1):
            return Recommendation.buy
        else:
            return Recommendation.neutral

    def MACD_CALCULATION(macd, signal):
        """Compute Moving Average Convergence/Divergence

        Args:
            macd (float): MACD.macd value
            signal (float): MACD.signal value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (macd > signal):
            return Recommendation.buy
        elif (macd < signal):
            return Recommendation.sell
        else:
            return Recommendation.neutral
        
    
    def Default_CALCULATION(value):
        """Compute Simple

        Args:
            value (float): Rec.X value

        Returns:
            string: "BUY", "SELL", or "NEUTRAL"
        """
        if (value == -1):
            return Recommendation.sell
        elif (value == 1):
            return Recommendation.buy
        else:
            return Recommendation.neutral
