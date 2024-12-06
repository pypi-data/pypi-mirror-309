import warnings

import numpy as np
from scipy.optimize import minimize


class util_rc:
    """
        Args:
        :param modeltype: a string describing the model to fit data:
            "E" for expected utility where U = p * A^alpha
            "R" for risk-return where U = EV - b * Var
            "W" for weber where U = EV - b *CV and CV = sqrt(Var)/EV1
            "H" for hyperbolic where U = A/(1+h*theta) and theta = (1-p)/p
        :param choice: an array-like of size n containing only the values 1 and 0, where 1 represents choosing option 1 and 0 represents option2
        :param amt1: an array-like of size n containing non-negative numbers, where each value represents the payoffs for option 1
        :param prob1: an array-like of size n containing non-negative number between 0 and 1, where each value represents the probability of winning amt1
        :param amt2: an array-like of size n containing non-negative numbers, where each value represents the payoffs for option 2
        :param prob2: an array-like of size n containing non-negative number between 0 and 1, where each value represents the probability of winning amt2

        Validates the inputs and fits the chosen modeltype to the binary risky choice data.

        Stores and outputs parameters in an instance variable named params, a python list containing:
            fitted_param: the parameter that maximizes likelihood of choice data (solves for alpha for EUT, b for Risk-Return, b for Weber, or h for Hyperbolic)
            inv_temp: inverse temperature, the estimated level of randomness in choices
            fit_metrics: Sequential Least Squares Programming (SLSQP)
            modeltype: the model type the user inputted
            num_observations: the number of observations, n

        if all input data is one-sided, the parameter is calculated only at the min or max, and params is instead formatted as [fitted_param, likelihood, fit_metrics, modeltype, num_observations]
        """

    def __init__(self, modeltype, choice, amt1, prob1, amt2, prob2):

        if not len(choice) == len(amt1) == len(amt2) == len(prob1) == len(prob2):
            raise ValueError('all vectors must have the same length')

        # check model type
        if not isinstance(modeltype, str):
            raise TypeError('modeltype must be a string')
        elif modeltype.upper() not in ["E", "R", "W", "H"]:
            raise Exception("modeltype must be E for expected utility theory, R for risk-return, W for weber, "
                            "or H for hyperbolic")
        else:
            self.modeltype = modeltype

        # check choice
        if not isinstance(choice, np.ndarray):
            try:
                choice = np.array(choice)
            except Exception:
                raise Exception("choice must be array like object")
        try:
            choice = choice.astype(float)
        except Exception:
            raise Exception("choice must be numbers")
        if not set(choice) <= {0, 1}:
            raise Exception("choice must only consists of 0 and 1 where 1 is choosing option 1 and 0 is choosing "
                            "option2")
        else:
            self.choice = choice

        # check amounts
        if not (isinstance(amt1, np.ndarray)):
            try:
                amt1 = np.array(amt1)
            except Exception:
                raise Exception("amount must be array like object")
        if not (isinstance(amt2, np.ndarray)):
            try:
                amt2 = np.array(amt2)
            except Exception:
                raise Exception("amount must be array like object")
        try:
            amt1 = amt1.astype(float)
            amt2 = amt2.astype(float)
        except Exception:
            raise Exception("amounts must be numbers")
        if any([x <= 0 for x in amt1]) or any([x <= 0 for x in amt2]):
            raise Exception("amounts must be positive")
        elif len(amt1) < 3:
            raise Exception("must have at least 3 observations")
        else:
            self.amt1 = amt1
            self.amt2 = amt2

        # check probabilities
        if not (isinstance(prob1, np.ndarray)):
            try:
                prob1 = np.array(prob1)
            except Exception:
                raise Exception("probabilities must be array like object")
        if not (isinstance(prob2, np.ndarray)):
            try:
                prob2 = np.array(prob2)
            except Exception:
                raise Exception("probabilities must be array like object")
        try:
            prob1 = prob1.astype(float)
            prob2 = prob2.astype(float)
        except Exception:
            raise Exception("probabilities must be numbers")
        if any([x <= 0 or x > 1 for x in prob1]) or any([x <= 0 or x > 1 for x in prob2]):
            raise Exception("probabilities must be between 0 (exclusive) and 1 (inclusive)")
        else:
            self.prob2 = prob2
            self.prob1 = prob1
        if all(self.choice) or not any(self.choice):
            warnings.warn("all input data is one-sided")
            self.params = self.flagged()
        else:
            self.params = self.min_func()
            self.predict()

        self.params = self.min_func()
        self.predict()
            # print(f""
            # fitted parameter: {self.params[0]}
            # inverse temperature: {self.params[1]}
            # fit metrics: {self.params[2]}
            # model type: {self.params[3]}
            # num of observations: {self.params[4]}
            # """)

    def flagged(self):
        """
        function is called when all input data is one-sided to calculate the minimum and maximum parameter and their likelhood.

        :return: the parameter with the higher likelihood, formatted as [parameter, likelihood, fit_metrics, model, num_obs]
        """
        num_obs = len(self.amt1)
        fit_metrics = "n/a"
        if self.modeltype == "E":
            bounds = self.e_bounds()
            util_min = self.eut(bounds[0][0])
            util_max = self.eut(bounds[0][1])
            like1 = self.avg_like(util_min)
            like2 = self.avg_like(util_max)
            model = "Expected Utility Theory"
            if like1 > like2:
                return[bounds[0][0], like1, fit_metrics, model, num_obs]
            return [bounds[0][1], like2, fit_metrics, model, num_obs]
        elif self.modeltype == "R":
            bounds = self.r_bounds()
            util_min = self.risk_return(bounds[0][0])
            util_max = self.risk_return(bounds[0][1])
            like1 = self.avg_like(util_min)
            like2 = self.avg_like(util_max)
            model = "Risk Return"
            if like1 > like2:
                return[bounds[0][0], like1, fit_metrics, model, num_obs]
            return [bounds[0][1], like2, fit_metrics, model, num_obs]
        elif self.modeltype == "W":
            bounds = self.w_bounds()
            util_min = self.co_of_var(bounds[0][0])
            util_max = self.co_of_var(bounds[0][1])
            like1 = self.avg_like(util_min)
            like2 = self.avg_like(util_max)
            model = "Weber"
            if like1 > like2:
                return[bounds[0][0], like1, fit_metrics, model, num_obs]
            return [bounds[0][1], like2, fit_metrics, model, num_obs]
        else:
            bounds = self.h_bounds()
            util_min = self.prob_discount(bounds[0][0])
            util_max = self.prob_discount(bounds[0][1])
            like1 = self.avg_like(util_min)
            like2 = self.avg_like(util_max)
            model = "Hyperbolic"
            if like1 > like2:
                return[bounds[0][0], like1, fit_metrics, model, num_obs]
            return [bounds[0][1], like2, fit_metrics, model, num_obs]
    def predict(self):
        """
        uses the fitted parameter to predict choices to check if fitted model will predict one-sided choices
        """
        if self.modeltype == "E":
            util = self.eut(self.params[0])
        elif self.modeltype == "R":
            util = self.risk_return(self.params[0])
        elif self.modeltype == "W":
            util = self.co_of_var(self.params[0])
        else:
            util = self.prob_discount(self.params[0])
        if all(util < 0) or all(util > 0):
            warnings.warn("fitted model predicts that all choices are one sided")
            # also return parameter bounds and log likelihood

    def ev_var(self, am, prob):
        """
        :param am: array-like of size n that represents the payoff amount
        :param prob: array-like of size n that represents the probability
        :return: [expected value, variance]
        """
        ev = am * prob
        var = prob * (am - ev) ** 2 + (1 - prob) * (-ev) ** 2
        return [ev, var]

    # expected utility theory E
    def eut(self, a):
        """
        :param a: expected utility theory parameter
        :return: the difference in eut utility calculated using a and the amounts and probabilities arrays for option1 and optoin2
        """
        return ((self.amt2 ** a) * self.prob2) - ((self.amt1 ** a) * self.prob1)

    # Risk Return R
    def risk_return(self, b):
        """

        :param b: risk return parameter
        :return: the difference in risk return utility calculated with b and the amounts and probabilities arrays for option1 and optoin2
        """
        option1 = self.ev_var(self.amt1, self.prob1)
        option2 = self.ev_var(self.amt2, self.prob2)
        return option2[0] - b * option2[1] - (option1[0] - b * option1[1])

    # Weber (coefficient of variation) W
    def co_of_var(self, b):
        """

        :param b: Weber (coefficient of variation) parameter
        :return: the difference Weber utility calculated with b and the amounts and probabilities arrays for option1 and optoin2
        """
        option1 = self.ev_var(self.amt1, self.prob1)
        option2 = self.ev_var(self.amt2, self.prob2)
        return option2[0] - b * np.sqrt(option2[1]) / option2[0] - (option1[0] - b * np.sqrt(option1[1]) / option1[0])

    # Hyperbolic H
    def prob_discount(self, h):
        """

        :param h: Hyperbolic parameter
        :return: the difference Hyperbolic utility calculated with h and the amounts and probabilities arrays for option1 and optoin2
        """
        theta1 = (1 - self.prob1) / self.prob1
        theta2 = (1 - self.prob2) / self.prob2
        return (self.amt2 / (1 + h * theta2)) - (self.amt1 / (1 + h * theta1))

    def parent_func(self, target, inv_temp):
        """

        :param target: the predicted parameter
        :param inv_temp: inverse temperature
        :return: log likelihood of the predicted parameter
        """
        if self.modeltype == "E":
            DV1 = self.eut(np.exp(target))
        elif self.modeltype == "R":
            DV1 = self.risk_return(target)
        elif self.modeltype == "W":
            DV1 = self.co_of_var(target)
        else:
            DV1 = self.prob_discount(np.exp(target))
        DV2 = -np.array([DV1[i] if not self.choice[i] else -DV1[i] for i in np.arange(len(DV1))])
        DV3 = DV2/np.exp(inv_temp)
        # util_2 - util_1 if choose option2 (0) else util_1 - util2 (choose option1)
        log_p = [-np.log(1 + np.exp(DV3[i])) if DV3[i] < 709 else -DV3[i] for i in np.arange(len(DV3))]
        return -np.sum(log_p)

    # minimize
    def avg_like(self, util_diff):
        """

        :param util_diff: an array-like object containing the difference in utility between option1 and option2
        :return: the average likelihood
        """
        logit = 1/(1+np.exp(-util_diff))
        likelihood = (1-self.choice) * logit + (1-logit)*(self.choice)
        # util_diff is choice 2 - choice logit is for choice 2, which is 0
        likelihood2 = [x if x != 0 else np.exp(-307) for x in likelihood]
        return np.mean(likelihood2)
    def min_func(self):
        """
        computes the fitted parameter by using multiple starting points calculated using the bounds and stores the parameter and inverse temperature with the highest likelihood
        :return: [fitted_param, inv_temp, fit_metrics, model, num_obs]
        """
        def startingpoints(start,end):
            range = end - start
            incr = range/4
            return[start + incr, start + 2*incr, start + 3*incr]

        func = lambda a: self.parent_func(a[0], a[1])
        likelihoods = np.array([])
        params = np.array([])
        invtemps = np.array([])
        if self.modeltype == "E":
            model = "Expected Utility Theory"
            bound = self.e_bounds()
            start = startingpoints(bound[0][0], bound[0][1])
            for i in np.arange(0, 3):
                fitted = minimize(func, [start[i], 0], method='SLSQP', bounds=bound + [(0, 37)])
                a = np.exp(fitted.x[0])
                util_diff = self.eut(a)
                # like = self.avg_like(util_diff)
                likelihoods = np.append(likelihoods, self.avg_like(util_diff))
                params = np.append(params, a)
                invtemps = np.append(invtemps,fitted.x[1])
            fitted_param = params[np.argmax(likelihoods)]
            inv_temp = invtemps[np.argmax(likelihoods)]
        elif self.modeltype == "R":
            model = "Risk Return"
            bound = self.r_bounds()
            start = startingpoints(bound[0][0], bound[0][1])
            for i in np.arange(0, 3):
                fitted = minimize(func, [start[i], 0], method='SLSQP', bounds= bound + [(0, 37)])
                b = fitted.x[0]
                util_diff = self.risk_return(b)
                like = self.avg_like(util_diff)
                likelihoods = np.append(likelihoods, like)
                params = np.append(params, b)
                invtemps = np.append(invtemps,fitted.x[1])
            fitted_param = params[np.argmax(likelihoods)]
            inv_temp = invtemps[np.argmax(likelihoods)]
        elif self.modeltype == "W":
            model = "Weber"
            bound = self.w_bounds()
            start = startingpoints(bound[0][0], bound[0][1])
            for i in np.arange(0, 3):
                fitted = minimize(func, [start[i], 0], method='SLSQP', bounds= bound +[(0,37)])
                b = fitted.x[0]
                util_diff = self.co_of_var(b)
                like = self.avg_like(util_diff)
                likelihoods = np.append(likelihoods, like)
                params = np.append(params, b)
                invtemps = np.append(invtemps,fitted.x[1])
            fitted_param = params[np.argmax(likelihoods)]
            inv_temp = invtemps[np.argmax(likelihoods)]
        else:
            model = "Hyperbolic"
            bound = self.h_bounds()
            start = startingpoints(bound[0][0], bound[0][1])
            for i in np.arange(0, 3):
                fitted = minimize(func, [start[i], 0], method='SLSQP', bounds= bound +[(0,37)])
                h = np.exp(fitted.x[0])
                util_diff = self.prob_discount(h)
                like = self.avg_like(util_diff)
                likelihoods = np.append(likelihoods, like)
                params = np.append(params, h)
                invtemps = np.append(invtemps,fitted.x[1])
            fitted_param = params[np.argmax(likelihoods)]
            inv_temp = invtemps[np.argmax(likelihoods)]
        fit_metrics = "SLSQP"
        num_obs = len(self.amt1)
        return [fitted_param, inv_temp, fit_metrics, model, num_obs]

    def e_bounds(self):
        """
        calculates the possible parameters using prob2, prob1, amt1, amt2 in log space
        :return: the minimum and maximum value for expected utility theory parameter alpha
        """
        a = np.log(self.prob2/self.prob1)/(np.log(self.amt1/self.amt2))
        #
        # errors when denominator = 0
        # if take log(1)
        # if prob2 = prob1
        return [(np.log(min(a)), np.log(max(a)))]

    def r_bounds(self):
        """
        calculates the possible parameters for risk return using prob2, prob1, amt1, amt2, filtering for when variance of option1 and option2 are the same
        :return: the minimum and maximum value for risk-return parameter b
        """
        option1 = self.ev_var(self.amt1, self.prob1)
        option2 = self.ev_var(self.amt2, self.prob2)
        filtered = self.exclude(option1, option2)

        # if var are the same, exclude from calculating bounds
        b = (filtered[0][0] - filtered[1][0]) / (filtered[0][1] - filtered[1][1])
        return [(min(b), max(b))]

    def exclude(self,opt1,opt2):
        """
        :param opt1: an array-like of size n
        :param opt2: an array-like of size n

        remove instances where the value at index i of opt1 is the same as the value at index i of opt 2

        :return: a nested list of [opt1,opt2] where duplicates are removed
        """
        i = 0
        same_index = np.where(opt1[1] == opt2[1])[0]
        for i in same_index:
            np.delete(opt1[1],i)
            np.delete(opt1[0],i)
            np.delete(opt2[1],i)
            np.delete(opt2[1],i)
            same_index.remove(i)
            same_index = same_index - 1
        return [opt1, opt2]

    def w_bounds(self):
        """
        calculates the possible parameters for Weber's coefficient of variation using prob2, prob1, amt1, amt2, filtering for when variance of option1 and option2 are the same
        :return: the minimum and maximum value for Weber parameter b
        """
        option1 = self.ev_var(self.amt1, self.prob1)
        option2 = self.ev_var(self.amt2, self.prob2)
        # if var are the same, exclude
        filtered = self.exclude(option1,option2)
        b = (filtered[0][0] - filtered[1][0]) / ((np.sqrt(filtered[0][1]) / filtered[0][0]) - (np.sqrt(filtered[1][1]) / filtered[1][0]))
        return [(min(b), max(b))]

    def h_bounds(self):
        """
        calculates the possible parameters for hypberbolic model using prob2, prob1, amt1, amt2, filtering for when amt1 divided by odds ratio of option2 is equal to amt2 divided by odds ratio of option1
        :return: the minimum and maximum possible value for Hyperbolic parameter H
        """
        theta1 = (1 - self.prob1) / self.prob1
        theta2 = (1 - self.prob2) / self.prob2
        opt1 = [self.amt1, self.amt1*theta2]
        opt2 = [self.amt2, self.amt2*theta1]
        filtered = self.exclude(opt1, opt2)
        h = (filtered[1][0] - filtered[0][0])/(filtered[0][1] - filtered[1][1])
        # h = (A2 - A1)/(A1*theta2 - A2*theta1)
        # exclude when demoniator is 0
        return [(np.log(min(h)), np.log(max(h)))]