#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © ${year} ${dev_name} ${dev_email}
#
# Distributed under terms of the GPL license.
"""Operator Charm main library."""
# Load modules from lib directory
import logging

import setuppath  # noqa:F401,I102
import yaml
from jinja2 import Environment, FileSystemLoader
from oci.oci_image import OCIImageResource
from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus


class ${class}(CharmBase):
    """Class reprisenting this Operator charm."""

    state = StoredState()

    def __init__(self, *args):
        """Initialize charm and configure states and events to observe."""
        super().__init__(*args)
        # -- standard hook observation
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.start, self.on_start)
        # -- initialize states --
        self.state.set_default(installed=False)
        self.state.set_default(configured=False)
        self.state.set_default(started=False)
        # -- Setup Jinja --
        loader = FileSystemLoader(self.charm_dir / 'templates')
        self.jinja_environemnt = Environment(loader=loader)

    # Starting in juju 2.8
    def on_install(self, event):
        """Handle install state."""
        self.unit.status = MaintenanceStatus("Installing charm software")
        # Perform install tasks
        self.unit.status = MaintenanceStatus("Install complete")
        logging.info("Install of software complete")
        self.state.installed = True

    def on_config_changed(self, event):
        """Handle config changed."""
        image = OCIImageResource(self, "image")
        image_info = image.fetch()

        template = self.jinja_environemnt.get_template('pod_spec.yaml')
        ctx = {
          'image_path': image_info.image_path,
          'repo_username': image_info.username,
          'repo_password': image_info.password,
        }
        pod_spec = yaml.safe_load(template.render(ctx))
        logging.debug(f"Using pod_spec: {pod_spec}")
        self.model.pod.set_spec(pod_spec)

        self.state.configured = True

    def on_start(self, event):
        """Handle start state."""

        if not self.state.configured:
            logging.warning("Start called before configuration complete, deferring event: {}".format(event.handle))
            self._defer_once(event)

            return
        self.unit.status = MaintenanceStatus("Starting charm software")
        # Start software
        self.unit.status = ActiveStatus("Unit is ready")
        self.state.started = True
        logging.info("Started")

    def _defer_once(self, event):
        """Defer the given event, but only once."""
        notice_count = 0
        handle = str(event.handle)

        for event_path, _, _ in self.framework._storage.notices(None):
            if event_path.startswith(handle.split('[')[0]):
                notice_count += 1
                logging.debug("Found event: {} x {}".format(event_path, notice_count))

        if notice_count > 1:
            logging.debug("Not deferring {} notice count of {}".format(handle, notice_count))
        else:
            logging.debug("Deferring {} notice count of {}".format(handle, notice_count))
            event.defer()


if __name__ == "__main__":
    main(${class})
