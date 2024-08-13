const formatNumberToLanguage = (number) => {
	const formattedNumber = new Intl.NumberFormat(language).format(number);
	return formattedNumber;
};
