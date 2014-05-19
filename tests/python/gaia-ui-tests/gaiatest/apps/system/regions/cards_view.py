# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette.marionette import Actions

from gaiatest.apps.base import Base


class CardsView(Base):

    # Home/Cards view locators
    _cards_view_locator = (By.CSS_SELECTOR, '#screen.cards-view:not(.edges)')
    # Check that the origin contains the current app name, origin is in the format:
    # app://clock.gaiamobile.org
    _apps_cards_locator = (By.CSS_SELECTOR, '#cards-view li[data-origin*="%s"]')
    _close_buttons_locator = (By.CSS_SELECTOR, '#cards-view li[data-origin*="%s"] .close-card')

    def _app_card_locator(self, app):
        return (self._apps_cards_locator[0], self._apps_cards_locator[1] % app.lower())

    def _close_button_locator(self, app):
        return (self._close_buttons_locator[0], self._close_buttons_locator[1] % app.lower())

    @property
    def is_cards_view_displayed(self):
        return self.is_element_displayed(*self._cards_view_locator)

    def _is_element_displayed_and_not_in_transition(self, by, locator):
        element = self.marionette.find_element(by, locator)
        return element.is_displayed() and 'transition' not in element.get_attribute('style')

    def is_app_displayed(self, app):
        # Close button needs also to be waited as it may be still moving
        # see https://bugzilla.mozilla.org/show_bug.cgi?id=1003175 for details
        return self._is_element_displayed_and_not_in_transition(*self._app_card_locator(app)) \
            and self._is_element_displayed_and_not_in_transition(*self._close_button_locator(app))

    def is_app_present(self, app):
        return self.is_element_present(*self._app_card_locator(app))

    def tap_app(self, app):
        self.wait_for_condition(lambda m: self.is_app_displayed(app))
        self.marionette.find_element(*self._app_card_locator(app)).tap()

    def close_app(self, app):
        self.wait_for_condition(lambda m: self.is_app_displayed(app))
        self.marionette.find_element(*self._close_button_locator(app)).tap()
        self.wait_for_element_not_present(*self._app_card_locator(app))

    def wait_for_cards_view(self):
        self.wait_for_element_displayed(*self._cards_view_locator)

    def wait_for_cards_view_not_displayed(self):
        self.wait_for_element_not_displayed(*self._cards_view_locator)

    def swipe_to_previous_app(self):
        current_frame = self.apps.displayed_app.frame

        final_x_position = current_frame.size['width']
        # start swipe from center of window
        start_x_position = final_x_position // 2
        start_y_position = current_frame.size['height'] // 2

        # swipe forward to get previous app card
        Actions(self.marionette).flick(
            current_frame, start_x_position, start_y_position, final_x_position, start_y_position).perform()
